from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.Signup.as_view(), name ='signup'),
    path('logout/', views.Signout.as_view(), name ='logout'),
    path('activate/', views.Activate.as_view(), name ='logout'),
]
