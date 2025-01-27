from django.urls import path
from accounts.views import RegisterView, UserDetailView, UserChangeView, UserPasswordChangeView
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/profile/', UserDetailView.as_view(), name='profile'),
    path('<int:pk>/profile/change/', UserChangeView.as_view(), name='profile_change'),
    path('<int:pk>/password/change/', UserPasswordChangeView.as_view(), name='password_change'),
]
