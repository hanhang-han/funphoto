from django.urls import path

from .views import *

app_name = 'photo'
urlpatterns = [
    path('register/',register,name='register'),
    path('register_code/',register_code,name='register_code'),
    path('',login,name='login'),
    path('index/',index,name ='index'),
    path('logout/',logout,name ='logout'),
    path('ownspace/',ownspace,name='ownspace'),
    path('uploadphoto/', uploadphoto, name='uploadphoto'),
    path('like/<photoid>/',like,name = 'like'),
    path('mylike/',mylike,name = 'mylike'),
    path('delete/<photoid>/',delete,name = 'delete'),
    path('refresh_captcha/', refresh_captcha),
    path('mynotifications/',mynotifications,name = 'mynotifications'),
    path('change_unread/',change_unread,name='change_unread'),
    path('change_read/', change_read, name='change_read'),
]