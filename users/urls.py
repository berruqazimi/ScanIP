from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('scan/', views.scan, name='scan'),
    path('pricing/', views.pricing, name='pricing'),
    path('users/', views.appusers_list, name='appusers-list'),
    path('users/<int:pk>/', views.appusers_detail, name='appusers-detail'),
]
