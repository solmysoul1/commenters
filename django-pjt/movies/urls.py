from django.urls import path
from . import views

urlpatterns = [
    # path('database/genre/', views.database_genre_list),
    # path('database/movie/', views.database_movie_list),
    # path('database/movie/detail/', views.database_movie_detail),
    # path('database/review_Naver/', views.database_review_Naver),
    # path('database/review_AI/', views.database_review_AI),
    # path('database/popular/', views.database_popular_list),
    # path('database/top/', views.database_top_list),
    # path('database/now/', views.database_now_list),
    path('search/', views.search),
    path('sub_color/<str:movie_color>/', views.sub_color_list),
    path('movie_list/', views.movie_list),
    path('movie/<int:movie_pk>/', views.movie_detail),
    path('genre_list/', views.genre_list),
    path('genre/<int:genre_id>/', views.genre_movies),
    path('review_list/', views.review_list),
    path('review/<int:review_pk>/like/', views.review_like),
    path('detail/<int:movie_pk>/likelist/', views.movie_like),
    path('detail/<int:movie_pk>/dislikelist/', views.movie_dislike),
    path('detail/<int:movie_pk>/watchlist/', views.movie_watchlist),
    path('detail/<int:movie_pk>/create_review/', views.create_review),
    path('detail/<int:review_pk>/delete_review/', views.delete_review),
    path('detail/<int:review_pk>/update_review/', views.update_review),
    path('main_recommendation/', views.main_recommendation),
    path('watchlist_or_recommendation/', views.watchlist_or_recommendation),
]
