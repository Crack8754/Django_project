from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('products/', views.products, name='products'),
    path('create/', views.create_product, name='create'),
    path('profile/', views.profile, name='profile'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

]


