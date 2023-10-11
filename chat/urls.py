# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    #  path('<str:room_name>/', views.room, name='room'),
    path('chat/messages/<int:user_id>/<int:student_id>/', views.UserDoctorChatView.as_view(), name='user-doctor-chat'),
    path('chat/create/',views.MessageCreateView.as_view(),name='message-create'),
    path('users-chatted-with/<int:user_id>/', views.UsersChattedWithView.as_view(), name='users-chatted-with'),

]