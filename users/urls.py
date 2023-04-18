from django.urls import path
from . import views
#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.users, name="users"),
    path('auth', views.authenticate, name="auth"),
    #path('register', registration_view, name="register"),
    #path('login', obtain_auth_token, name="register"),
]