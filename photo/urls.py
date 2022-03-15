from django.urls import path

from .views import *
urlpatterns = [
    path('register/',register,name='register'),
    path('register_code/',register_code,name='register_code'),
    path('',login,name='login'),

]