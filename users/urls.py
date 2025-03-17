from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, PasswordChangeView, UserProfileView, LogoutView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout_all'),
]
