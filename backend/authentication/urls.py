from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('check-email/', views.check_email, name='check_email'),
]
