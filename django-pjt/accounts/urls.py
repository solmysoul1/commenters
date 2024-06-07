from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('delete/', views.delete_account),
    path('user/', views.get_user),
    path('profile/<int:user_pk>/', views.profile_read),
    path('profile/<int:user_pk>/likelist/', views.like_list),
    path('profile/<int:user_pk>/dislikelist/', views.dislike_list),
    path('profile/<int:user_pk>/watchlist/', views.watch_list),
    path('<int:user_pk>/follow/', views.follow),
    path('<int:user_pk>/update/', views.profile_update),
    path('<int:user_pk>/password/change/', views.password_change),
]
