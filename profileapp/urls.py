from django.urls import path
from .views import *
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
]
