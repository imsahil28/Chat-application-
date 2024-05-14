from django.contrib import admin
from django.urls import path,include
from .views import *
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,  home  , name="home"),
    path('login/', views.login_user, name='login'), 
    path('register/',register_user ,name='register_user'),
    path('token_send/',token_send ,name='token_send'),
    path('verify/<str:auth_token>/', verify, name="verify"),    
    path('sucess/',sucess ,name='sucess'),
    path('error/',error ,name='error'),
    path("__reload__/", include("django_browser_reload.urls")),   
    path('user/',views.user ,name='user'),
    path("<str:slug>/", views.room, name='room'),    
]