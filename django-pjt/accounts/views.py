from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import FollowSerializer, ProfileSerializer, UserSerializer, MovieSerializer
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    request.user.delete()
    data = {
        'content': f'{request.user}님의 탈퇴처리가 완료되었습니다.',
    }
    return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def follow(request, user_pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error":"로그인이 필요합니다."})
    
    follow_user = get_object_or_404(User, pk=user_pk)
    user = request.user
    if follow_user != user:
        if user in follow_user.followers.all():
            follow_user.followers.remove(user)
            is_following = False
        else:
            follow_user.followers.add(user)
            is_following = True
        
        serializer = FollowSerializer(follow_user)
        data = serializer.data
        data['is_following'] = is_following
        return Response(data, status=status.HTTP_200_OK)
    return Response({"error":"자기 자신을 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 프로필 페이지에 출력할 유저 프로필 정보 받아오기
# 로그인된 사용자이어야 할 필요가 없어서 따로 분리함 (논의 필요!)
@api_view(['GET'])
def profile_read(request, user_pk):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=user_pk)
        serializer = ProfileSerializer(user)
        data = serializer.data

        # 로그인된 사용자와 프로필 페이지의 사용자가 같은지 여부를 확인
        # request.user는 현재 로그인된 사용자를 나타냅니다.
        # 비로그인 상태일 경우 request.user는 AnonymousUser 객체가 됩니다.
        if request.user.is_authenticated:
            if request.user.pk == user.pk:
                data['is_self'] = True
                data['is_following'] = False
            
            elif request.user in user.followers.all():
                data['is_self'] = False
                data['is_following'] = True
        else:
            data['is_self'] = False
            data['is_following'] = False

        return Response(data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'success': False}, status = 405 )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.user == user:
        serializer = ProfileSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('access denied', status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request, user_pk):
    user = request.user
    form = PasswordChangeForm(user, request.data)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return Response('비밀번호 변경 완료', status=status.HTTP_200_OK)
    else:
        errors = form.errors.get_json_data()
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def like_list(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        like_movies = user.like_movies.all()
        serializer = MovieSerializer(like_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def dislike_list(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        dislike_movies = user.dislike_movies.all()
        serializer = MovieSerializer(dislike_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def watch_list(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        watchlist_movies = user.watchlist_movies.all()
        serializer = MovieSerializer(watchlist_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Method Not Allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)






