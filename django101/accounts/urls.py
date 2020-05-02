from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('product/', views.products),
    path('customer/<str:pk_test>/', views.customer),
]