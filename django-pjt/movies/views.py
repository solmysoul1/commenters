# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from tqdm import tqdm
# from collections import deque
# import random
# import pyperclip
# import pickle
# from django.db.models import Max
# from tkinter.tix import Tree
# import requests
# import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework import status
from django.db.models import Count, Q
from .models import Genre, Movie, Review
from .serializers import MovieListSerializer, MovieSerializer, ReviewListSerializer, GenreListSerializer, ReviewSerializer
from django.db.models import Q
import pathlib
import textwrap

# import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown

# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

User = get_user_model()

# 팔로워 기반 핵심 추천 알고리즘
@api_view(['GET'])
def main_recommendation(request):
    if request.method == 'GET':
        # 추천 영화를 담을 리스트
        recommended_movies = []
        
        # 0단계: 가장 vote_average가 높은 영화 8개 목록을 만든다
        top_movies = Movie.objects.order_by('-vote_average')[:8]
        
        # 로그인한 유저라면
        if request.user.is_authenticated:
            user = request.user

            # 2-1단계: 팔로우한 리뷰어들 중, 나랑 평가한 영화가 가장 많이 겹치는 리뷰어부터 고려해서,
            # 그 리뷰어가 좋게 평가한 영화 (8점 이상) 중 내가 보지 않았고 싫어하지 않은 영화들을 최대 8개까지 출력
            followed_reviewers = user.followings.all()

            # 평가한 영화가 가장 많이 겹치는 리뷰어들을 찾기
            reviewer_scores = User.objects.filter(
                review__movie__review__user=user,
                id__in=followed_reviewers.values_list('id', flat=True)
            ).annotate(
                common_reviews=Count('review', filter=Q(review__movie__review__user=user))
            ).order_by('-common_reviews')
            
            # 리뷰어가 좋게 평가한 영화 (8점 이상) 중 내가 보지 않았고 싫어하지 않은 영화들을 최대 8개까지 출력
            for reviewer in reviewer_scores:
                movies_level_1 = Movie.objects.filter(
                    review__user=reviewer,
                    review__rating__gte=8
                ).exclude(
                    review__user=user
                ).exclude(
                    dislike_users=user
                ).exclude(
                    id__in=[movie.id for movie in recommended_movies]
                ).order_by('-vote_average')[:8 - len(recommended_movies)]
                
                for movie in movies_level_1:
                    if movie not in recommended_movies and len(recommended_movies) < 8:
                        recommended_movies.append(movie)
                    if len(recommended_movies) >= 8:
                        break

            # 2-2단계: 1번에서 출력된 전체 목록이 8개 미달일 경우, 가장 인기있는 리뷰어들(팔로잉이 많은 순으로 정렬)에서
            # 동일하게 그 리뷰어가 평가를 좋게 한 작품들 (8점 이상) 중 내가 평가하지 않았고 싫어하지 않은 작품들을 최대 8개까지 목록 선정 후 출력함
            if len(recommended_movies) < 8:
                popular_reviewers = User.objects.annotate(
                    followers_count=Count('followers')
                ).order_by('-followers_count')[:5]  # 예시로 5명의 인기 리뷰어 선택
                
                more_movies = Movie.objects.filter(
                    review__user__in=popular_reviewers,
                    review__rating__gte=8
                ).exclude(
                    review__user=user
                ).exclude(
                    dislike_users=user
                ).exclude(
                    id__in=[movie.id for movie in recommended_movies]
                ).order_by('-vote_average')[:8 - len(recommended_movies)]
                
                for movie in more_movies:
                    if movie not in recommended_movies and len(recommended_movies) < 8:
                        recommended_movies.append(movie)
                    if len(recommended_movies) >= 8:
                        break

            # 2-3단계: 2-2의 결과가 8개가 안되면 8개가 될 때까지 0번에서 만들어진 목록에서 영화를 넣어 출력한다
            if len(recommended_movies) < 8:
                remaining_movies = [movie for movie in top_movies if movie not in recommended_movies]
                for movie in remaining_movies:
                    if movie not in recommended_movies and len(recommended_movies) < 8:
                        recommended_movies.append(movie)
                    if len(recommended_movies) >= 8:
                        break

        else:
            # 로그인하지 않은 사용자의 경우 0번에서 만들어진 목록을 그대로 사용하여 출력한다
            recommended_movies = top_movies

        serializer = MovieSerializer(recommended_movies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 2. 워치리스트 출력 또는 다른 이용자들의 워치리스트 기반 추천
@api_view(['GET'])
def watchlist_or_recommendation(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            # 0. 로그인하지 않은 경우: watchlist_users가 가장 많은 영화 중 like_users가 가장 많은 영화 8개를 가져온다.
            top_movies = Movie.objects.annotate(
                watchlist_count=Count('watchlist_users', distinct=True),
                like_count=Count('like_users', distinct=True)
            ).order_by('-watchlist_count', '-like_count')[:8]
            serializer = MovieSerializer(top_movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = request.user
            if user.watchlist_movies.exists():
                # 1. 로그인한 경우: user의 워치리스트에 추가한 영화들 중 watchlist_users가 가장 많고, 그 중 like_users가 가장 많은 영화들을 최대 8개 반환한다.
                watchlist_movies = user.watchlist_movies.all()
                user_watchlist_movie_ids = watchlist_movies.values_list('id', flat=True)
                top_watchlist_movies = Movie.objects.filter(id__in=user_watchlist_movie_ids).annotate(
                    watchlist_count=Count('watchlist_users', distinct=True),
                    like_count=Count('like_users', distinct=True)
                ).order_by('-watchlist_count', '-like_count')[:8]
                serializer = MovieSerializer(top_watchlist_movies, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # 2. 내 워치리스트에 영화가 없을 경우: 전체 영화 중에서 내가 싫어요하지 않았고, 내가 평가하지 않은 영화들 중 watchlist_users와 like_users가 많은 상위 8개 영화를 반환한다.
                top_movies = Movie.objects.exclude(
                    dislike_users=user
                ).exclude(
                    watchlist_users=user
                ).annotate(
                    watchlist_count=Count('watchlist_users', distinct=True),
                    like_count=Count('like_users', distinct=True)
                ).order_by('-watchlist_count', '-like_count')[:8]
                serializer = MovieSerializer(top_movies, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)




# 영화 전체 리스트 출력, 메인페이지에 쓰일거라서 제목이랑 포스터 주소만 출력
@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 영화 상세 정보 출력, 넘겨 받은 movie_pk에 해당하는 영화 전체 정보 출력
# 해당하는 영화에 달린 review 들도 출력
# is_my_review 내가 리뷰를 달지 않은 영화는 False, 내가 리뷰를 단 영화일 경우 True를 전달
# my_review 내가 리뷰를 달지 않은 영화는 False, 내가 리뷰를 단 영화일 경우 해당 리뷰를 전달
# 리뷰를 돌면서 해당 리뷰를 작성한 작성자의 닉네임을 review_set에 추가 후 전달함
@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie, context={'request': request})
        data = serializer.data

        is_my_review = False
        for review in data['review_set']:
            
            user = get_object_or_404(User, pk=review['user'])
            review['user_nickname'] = user.nickname
            
            if request.user.id == review['user']:
                my_review = review
                is_my_review = True

        if not is_my_review:
            my_review = False
            
        data['my_review'] = my_review
        data['is_my_review'] = is_my_review
        
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# 장르 목록 출력 
@api_view(['GET'])
def genre_list(request):
    if request.method == 'GET':
        genres = get_list_or_404(Genre)
        serializer = GenreListSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 장르별 영화 목록 출력
@api_view(['GET'])
def genre_movies(request, genre_id):
    if request.method == 'GET':
        genre = get_object_or_404(Genre, id=genre_id)
        movies = genre.movie_set.all()
        serializer = MovieSerializer(movies, many=True)
        movies = serializer.data
        data = { 'movies': movies, 'genre': genre.name }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def sub_color_list(request, movie_color):
    if request.method == 'GET':
        movies = get_list_or_404(Movie, color=movie_color)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 영화 좋아요오
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
            is_like = False
        else:
            movie.like_users.add(request.user)
            is_like = True
        
        return JsonResponse({'success': True, 'like_users_count': movie.like_users.count(), 'is_like': is_like}, status = 200)
    else:
        return JsonResponse({'success': False}, status = 405 )

# 영화 싫어잇
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_dislike(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        if request.user in movie.dislike_users.all():
            movie.dislike_users.remove(request.user)
            is_dislike = False
        else:
            movie.dislike_users.add(request.user)
            is_dislike = True
        
        return JsonResponse({'success': True, 'dislike_users_count': movie.dislike_users.count(), 'is_dislike': is_dislike}, status = 200)
    else:
        return JsonResponse({'success': False}, status = 405 )

# 영화 볼거임
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_watchlist(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if request.method == 'POST':
        if not user.review_set.filter(movie=movie):

            if user in movie.watchlist_users.all():
                movie.watchlist_users.remove(user)
                is_watch = False
            
            else:
                movie.watchlist_users.add(user)
                is_watch = True
            
            return JsonResponse({'success': True, 'watchlist_users_count': movie.watchlist_users.count(), 'is_watch': is_watch}, status = 200)
        else:
            return JsonResponse({'success': False}, status = 403 )
    else:
        return JsonResponse({'success': False}, status = 405 )


# 리뷰를 라이크한다 ! 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        if request.user in review.like_users.all():
            review.like_users.remove(request.user)
            is_like = False
        else:
            review.like_users.add(request.user)
            is_like = True
        
        return JsonResponse({'success': True, 'like_users_count': review.like_users.count(), 'is_like': is_like}, status = 200)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 리뷰를 만들자
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, movie_pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        if movie.review_set.filter(user=user):
            return Response({'cannot create another review'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, movie=movie)
            if movie in user.watchlist_movies.all():
                user.watchlist_movies.remove(movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# 리뷰를 지운다
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_pk):
    if request.method == 'DELETE':
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('access denied', status=status.HTTP_403_FORBIDDEN)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# 리뷰를 수정한다
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_review(request, review_pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            serializer = ReviewSerializer(instance=review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('access denied', status=status.HTTP_403_FORBIDDEN)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 모든 리뷰 출력 
@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:100]
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 영화를 검색할거야
@api_view(['GET'])
def search(request):
    query = request.GET.get('q','')
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query) | Q(title__iregex=query))
        serializer = MovieSerializer(movies, many=True)
        return Response({'results' :serializer.data})

# DB에 리뷰를 넣기 위해 랜덤 유저를 추출하는 함수
# 해당 유저가 이미 해당 movie에 대한 리뷰를 작성했다면 다른 유저를 추출한다
def get_random_user(movie):
    max_id = User.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        user = User.objects.filter(pk=pk).first()
        if user:
            reviews = user.review_set.filter(movie=movie)
            if not reviews.exists():
                return user

# Google Gemini API를 통해 리뷰가 없는 영화들에 대한 리뷰 생성
# def database_review_AI(request):
    # GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    # genai.configure(api_key=GOOGLE_API_KEY)
    # model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # base_query = [{'role':'user', 'parts': ['이 다음 응답부터 보내주는 영화 정보를 통해 영화에 대해서 알아보고 평가를 5개 작성해줘. 별점(rating) : 자연수로 1~10 까지 가능해, 관람평(content) : rating에 맞는 영화에 대한 호평, 혹평 모두 가능하고 관람평은 중복 없이 100자 이내로 편한 인터넷에서 쓰는 반말로 작성해줘. ```json```을 붙이지 말구. 그냥 {"result": [{"rating": , "content": },{"rating": , "content": },...]}으로 출력해줘']}]
    # history = []
    # history.append(base_query[0])
    # response = model.generate_content(history)
    # history.append(response.candidates[0].content)

    # 리뷰가 3개 이하인 영화들을 불러와서 5개의 리뷰를 만들 예정
    # target_movies = Movie.objects.annotate(review_count=Count('review')).filter(review_count__lte=3)
    # print(target_movies.count())
    # for movie in target_movies:
    #     title = movie.title
    #     release_date = movie.release_date
    #     user_query = {'role':'user', 'parts': [f"영화제목: {title}, 개봉일: {release_date}"]}
    #     history.append(user_query)
    #     response = model.generate_content(history)
    #     history.append(response.candidates[0].content)
    #     time.sleep(3)
    #     print(response.text)
    #     result_json = json.loads(str(response.text))
    #     for each in result_json['result']:
    #         user = get_random_user(movie)
    #         Review.objects.get_or_create(
    #             user=user,
    #             movie=movie,
    #             content=each['content'],
    #             rating=int(each['rating']),
    #         )

    # return JsonResponse({ 'success': True })

    


# # 네이버 크롤링을 통해 리뷰를 가져오고, django-seed를 통해 만들어진 유저들 중 
# # 해당 영화에 대한 리뷰를 작성하지 않은 유저를 랜덤으로 추출하여,
# # 해당 영화에 대한 리뷰를 작성(create)하도록 함
# # 영화에 대한 리뷰가 네이버에서 조회되지 않는 경우, 리뷰 데이터 값이 끝난 경우의 에러는
# # try-except 를 사용하여 다음 정보를 조회하도록 함
# # 중복을 방지하기 위해 해당 content의 리뷰가 없을 경우에만 리뷰를 작성함
# def database_review_Naver(request):
#     op = webdriver.ChromeOptions()
#     chrome_service = ChromeService(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service = chrome_service, options=op)
    
#     movies = Movie.objects.all()
#     base_url='https://search.naver.com/search.naver?query='
#     max_id = User.objects.all().aggregate(max_id=Max("id"))['max_id']
    
#     for movie in movies:
#         if movie.review_set.count() > 0:
#             continue
#         else:
#             url = base_url+movie.title+' 관람평'
#             driver.get(url)
#             time.sleep(4)
#             for i in range(1, 20):
#                 content_location = f'//*[@id="main_pack"]/div[3]/div[2]/div/div/div[4]/div[4]/ul/li[{i}]'
#                 try: 
#                     content_elem = driver.find_element(By.XPATH, content_location)
#                     content = content_elem.get_attribute('data-report-title')
                    
#                     rating_location = content_location + '/div[1]/div/div[2]'
#                     rating_text = driver.find_element(By.XPATH, rating_location).text
#                     rating = int(rating_text[13:])
#                     if not Review.objects.filter(content=content):
#                         user = get_random_user(movie)
#                         Review.objects.get_or_create(
#                             user=user,
#                             movie=movie,
#                             content=content,
#                             rating=rating
#                         )
#                 except:
#                     continue

#     reviews = Review.objects.get(pk=1).values()
#     reviews_json = json.dumps(reviews)
#     return JsonResponse(reviews_json)

# def database_genre_list(request):
#     API_KEY = settings.TMDB_ACCESS_TOKEN

#     headers = {
#         'accept': 'application/json',
#         'Authorization': API_KEY
#     }

#     response = requests.get('https://api.themoviedb.org/3/genre/movie/list?language=ko', headers=headers)

#     if response.status_code == 200:
#         genre_data = response.json()

#         for result in genre_data.get('genres', []):
#             Genre.objects.get_or_create(
#                 id=result.get('id'),
#                 name=result.get('name')
#             )
        
#         return JsonResponse({'message': 'Genre data saved successfully'})
#     else:
#         # 에러 응답
#         return JsonResponse({'error': 'Failed to fetch genre data'}, status=500)


# def database_movie_list(request):
#     API_KEY = settings.TMDB_ACCESS_TOKEN

# # Create your views here.
#     headers = {
#         'accept': 'application/json',
#         'Authorization': API_KEY
#     }

#     response = requests.get('https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=ko-KR&page=1&sort_by=popularity.desc', headers=headers)

#     if response.status_code == 200:
#         movie_data = response.json()

#         for result in movie_data.get('results', []):

#             genre_ids = result.get('genre_ids', [])
#             genres = Genre.objects.filter(id__in=genre_ids)

#             movie, created = Movie.objects.update_or_create(
#                 tmdb_id=result.get('id'),
#                 defaults={
#                 'title':result.get('title'),    
#                 'adult':result.get('adult'),
#                 'poster_path':result.get('poster_path'),
#                 'backdrop_path':result.get('backdrop_path'),
#                 'vote_average':result.get('vote_average'),
#                 'release_date':result.get('release_date'),
#                 }
#             )
#             if created:
#                 movie.genres.add(*genres)
#         return JsonResponse({'message': 'Movie data saved successfully'})
#     else:
#         # 에러 응답
#         return JsonResponse({'error': 'Failed to fetch movie data'}, status=500)
    
# def database_movie_detail(request):
#     API_KEY = settings.TMDB_ACCESS_TOKEN

#     headers = {
#         'accept': 'application/json',
#         'Authorization': API_KEY
#     }

    # 키워드, 영화 제목으로 컬러 영화 받아오기
    # keyword = "Ponyo on the Cliff by the Sea"
    # color ='pink'
    # response = requests.get(f'https://api.themoviedb.org/3/search/movie?query={keyword}&include_adult=true&language=ko-KR&page=1', headers=headers)
        
    # if response.status_code == 200:
    #     movie_data = response.json()
    #     result_list = movie_data.get('results', [])
    #     result = result_list[0]

    #     genre_ids = result.get('genre_ids', [])
    #     genres = Genre.objects.filter(id__in=genre_ids)

    #     movie, created = Movie.objects.update_or_create(
    #         tmdb_id=result.get('id'),
    #         defaults={
    #         'title':result.get('title'),    
    #         'adult':result.get('adult'),
    #         'poster_path':result.get('poster_path'),
    #         'backdrop_path':result.get('backdrop_path'),
    #         'vote_average':result.get('vote_average'),
    #         'release_date':result.get('release_date'),
    #         'overview': '',
    #         'tagline': '',
    #         'runtime': 0,
    #         'color': color,
    #         }
    #     )
    #     if created:
    #         movie.genres.add(*genres)

    # 무비 디테일 업데이트
    # movies = Movie.objects.all()
    # for each in movies:
    #     response = requests.get(f'https://api.themoviedb.org/3/movie/{each.tmdb_id}?language=ko-KR', headers=headers)
        
    #     if response.status_code == 200:
    #         result = response.json()

    #         genre_ids = result.get('genre_ids', [])
    #         genres = Genre.objects.filter(id__in=genre_ids)

    #         movie, created = Movie.objects.update_or_create(
    #             tmdb_id=result.get('id'),
    #             defaults={
    #             'title':result.get('title'),    
    #             'adult':result.get('adult'),
    #             'poster_path':result.get('poster_path'),
    #             'backdrop_path':(result.get('backdrop_path') if result.get('backdrop_path') else ''),
    #             'vote_average':result.get('vote_average'),
    #             'release_date':result.get('release_date'),
    #             'overview': result.get('overview'),
    #             'tagline': result.get('tagline'),
    #             'runtime': result.get('runtime'),
    #             }
    #         )
    #         if created:
    #             movie.genres.add(*genres)
            
    # return JsonResponse({'message': 'Movie data saved successfully'})
    
    # else:
    #     # 에러 응답
    #     return JsonResponse({'error': 'Failed to fetch movie data'}, status=500)
    
# def database_popular_list(request):
#     API_KEY = settings.TMDB_ACCESS_TOKEN

#     headers = {
#         'accept': 'application/json',
#         'Authorization': API_KEY
#     }

#     for i in range(2, 10):
#         response = requests.get(f'https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={i}', headers=headers)

#         if response.status_code == 200:
#             movie_data = response.json()

#             for result in movie_data.get('results', []):
#                 genre_ids = result.get('genre_ids', [])
#                 genres = Genre.objects.filter(id__in=genre_ids)

#                 movie, created = Movie.objects.update_or_create(
#                     tmdb_id=result.get('id'),
#                     defaults={
#                     'title':result.get('title'),    
#                     'adult':result.get('adult'),
#                     'poster_path':result.get('poster_path'),
#                     'backdrop_path':(result.get('backdrop_path') if result.get('backdrop_path') else ''),
#                     'vote_average':result.get('vote_average'),
#                     'release_date':result.get('release_date'),
#                     'overview': result.get('overview'),
                    # 'tagline': '',
                    # 'runtime': 0,
                    # 'color': '',
#                     }
#                 )
#                 if created:
#                     movie.genres.add(*genres)
#     return JsonResponse({'message': 'Movie data saved successfully'})
    # else:
    #     # 에러 응답
    #     return JsonResponse({'error': 'Failed to fetch movie data'}, status=500)
    
# def database_top_list(request):
#     API_KEY = settings.TMDB_ACCESS_TOKEN

#     headers = {
#         'accept': 'application/json',
#         'Authorization': API_KEY
#     }

#     for i in range(2, 10):
#         response = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?language=ko-KR&page={i}', headers=headers)

#         if response.status_code == 200:
#             movie_data = response.json()

#             for result in movie_data.get('results', []):
#                 genre_ids = result.get('genre_ids', [])
#                 genres = Genre.objects.filter(id__in=genre_ids)

#                 movie, created = Movie.objects.update_or_create(
#                     tmdb_id=result.get('id'),
#                     defaults={
#                     'title':result.get('title'),    
#                     'adult':result.get('adult'),
#                     'poster_path':result.get('poster_path'),
#                     'backdrop_path':(result.get('backdrop_path') if result.get('backdrop_path') else ''),
#                     'vote_average':result.get('vote_average'),
#                     'release_date':result.get('release_date'),
#                     'tagline': '',
#                     'runtime': 0,
#                     'color': '',
#                     }
#                 )
#                 if created:
#                     movie.genres.add(*genres)
#     return JsonResponse({'message': 'Movie data saved successfully'})
    # else:
    #     # 에러 응답
    #     return JsonResponse({'error': 'Failed to fetch movie data'}, status=500)
    
# def database_now_list(request):
#     API_KEY = settings.TMDB_ACCESS_TOKEN

#     headers = {
#         'accept': 'application/json',
#         'Authorization': API_KEY
#     }

#     response = requests.get('https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&page=2', headers=headers)

#     if response.status_code == 200:
#         movie_data = response.json()

#         for result in movie_data.get('results', []):
#             genre_ids = result.get('genre_ids', [])
#             genres = Genre.objects.filter(id__in=genre_ids)

#             movie, created = Movie.objects.update_or_create(
#                 tmdb_id=result.get('id'),
#                 defaults={
#                 'title':result.get('title'),    
#                 'adult':result.get('adult'),
#                 'poster_path':result.get('poster_path'),
#                 'backdrop_path':result.get('backdrop_path'),
#                 'vote_average':result.get('vote_average'),
#                 'release_date':result.get('release_date'),
#                 }
#             )
#             if created:
#                 movie.genres.add(*genres)
#         return JsonResponse({'message': 'Movie data saved successfully'})
#     else:
#         # 에러 응답
#         return JsonResponse({'error': 'Failed to fetch movie data'}, status=500)
    