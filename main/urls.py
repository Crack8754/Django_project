from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('articles/', views.articles, name='articles'),
    path('create/', views.create_article, name='create'),
    path('profile/', views.profile, name='profile'),
]


