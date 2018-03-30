from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name="signup"),
    path('user/<str:username>', views.get_user_details, name='get_user_details'),
    path('like', views.like, name="like")
]