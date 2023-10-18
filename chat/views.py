from django.shortcuts import render
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .serializers import MessageSerializer
from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer 
from .models import Message
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async

# Create your views here.

def get_user_from_token(token_key):
    tok=token_key[6:]
    print(tok)
    try:
        print('yes')
        decoded_token = AccessToken(tok)
        user_id = decoded_token['user_id']
        print(user_id)

        return user_id
    except :
        return None

@database_sync_to_async
def update_online_status(status, user):
    try:    
        print(user)
        print('yyyy')
        user_obj=CustomUser.objects.get(id=user)
        print('yyyy11')
        user_obj.online = status
        user_obj.save()
    except:
        pass
    

class MessageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDoctorChatView(APIView):
    def get(self, request, user_id, student_id, *args, **kwargs):
        try:
            user_profile = CustomUser.objects.get(id=user_id)
            student_profile = CustomUser.objects.get(id=student_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "invalid user or doctor"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all messages related to the user and doctor
        messages = Message.objects.filter(
            (
                (models.Q(sender=user_profile) & models.Q(receiver=student_profile)) |
                (models.Q(sender=student_profile) & models.Q(receiver=user_profile))
            )
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
 
class UsersChattedWithView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Retrieve distinct combinations of sender and receiver IDs from Message model
        users_chatted_with = Message.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        ).exclude(sender=user).values('sender', 'receiver').distinct()

        # Extract unique user IDs from the combinations
        user_ids = set()
        for chat in users_chatted_with:
            user_ids.add(chat['sender'])
            user_ids.add(chat['receiver'])

        # Remove the current user's ID from the set
        user_ids.discard(user.id)

        # Fetch the corresponding users
        users = CustomUser.objects.filter(id__in=user_ids)

        # Serialize the list of users
        serializer = CustomUserSerializer(users, many=True)

        return Response(serializer.data, status=200)
    
class FetchOnlineView(APIView):
    def get(self,request,user_id):
        print(user_id)
        user=CustomUser.objects.get(id=user_id)
        online=user.online
        
        return Response(online,status=200)