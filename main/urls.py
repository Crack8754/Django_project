from django.urls import path
from .views import home, about
from . import views

urlpatterns = [
   path('', home, name='home'),
   path('about/', about, name='about'),
   path('register/', views.register, name='register'),
   path('login/', views.user_login, name='login'),
   path('create/', views.create_article, name='create'),
   path('articles/', views.articles, name='articles'),
]


