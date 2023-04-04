from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather, name="weather"),
    path('<int:limit>/', views.limit, name="getlimit"),
]