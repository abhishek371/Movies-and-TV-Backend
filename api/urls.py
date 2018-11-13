from django.urls import path

from . import views

urlpatterns = [
    path('auth/login', views.login, name="login"),
    path('auth/signup', views.signup, name="signup"),
    path('user/like/movie', views.like_movie, name="like_tv"),
    path('user/like/tv', views.like_tv, name="like_tv"),
    path('user/<str:username>', views.get_user_details, name="get_user_details"),
    path('movies', views.get_all_movies, name="get_movies"),
    path('movies/<str:movie_id>', views.get_movie_details, name="movie_details"),
    path('tv', views.get_all_tv, name="get_tv"),
    path('tv/<str:tv_id>', views.get_tv_details, name="tv_details"),
    path('irs/director/<str:query>', views.query_director, name="irs_director")
]
