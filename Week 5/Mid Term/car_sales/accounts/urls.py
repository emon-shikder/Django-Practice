from django.urls import path
from .views import register, user_login, user_profile, UserLogoutView, UserProfileUpdateView, user_logout
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='edit_profile'),
]
