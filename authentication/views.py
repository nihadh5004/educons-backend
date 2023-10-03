from django.http import JsonResponse
from django.views import View
from authentication.models import CustomUser  # Adjust the import path as needed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from backend import settings
from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.utils.encoding import force_bytes , force_str

# importing the token geneater which creates a unique hash value for user
from .token import generate_token

#for storing current time and user creation time
from datetime import timedelta
from django.utils import timezone


#for creating random values fo otp
import random

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    
    

class Signup(APIView):
     def post (self,request):
          try:
               username = request.data.get('username')
               email = request.data.get('email')
               password = request.data.get('password')

               

           # Check if the user with the given username or email already exists
               if CustomUser.objects.filter(username=username).exists():
                    return Response({'message': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

               # Create a new user object
               myuser=CustomUser.objects.create_user(username=username, password=password, email=email)
               myuser.is_active = False
               myuser.save()
               generated_otp=random.randint(100000,999999)
               generated_otp_test = request.session.get('otp')
               request.session['otp']=str(generated_otp)
               
               # sending OTP through mail
               subject = 'EduCons Confirmation OTP'
               message = f'Hello {myuser.username},\nWe are happy to serve you\n \nPlease Verify your account by OTP: {generated_otp}'
               from_email=settings.EMAIL_HOST_USER
               to_list=[myuser.email]
               
               send_mail(subject,message,from_email,to_list,fail_silently=True)

               return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
          except Exception as e:
               # Handle exceptions here and return an appropriate error response
               return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     # def get(self, request):
     #    otp=request.session.get('otp')
     #    print('otp',otp)
     #    users = CustomUser.objects.all()  # Retrieve all users
     #    user_serializer = CustomUserSerializer(users, many=True)  # Serialize the queryset
     #    return Response(user_serializer.data)  # Return serialized data


class Activate(APIView):
     
     def post(self, request):
          otp = request.data.get('otp')
          username = request.data.get('username')
          generated_otp = request.session.get('otp')
          print("Received OTP:", otp)
          print("Stored OTP:", generated_otp)
          if otp == generated_otp:
               try:
                    
                    myuser = CustomUser.objects.get(username=username)
                    myuser.is_active = True
                    myuser.save()
               except CustomUser.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
               
               # Delete the OTP from the session
               del request.session['otp']

               # You can send a success response with user data if needed
               # For example, you can send the user's username or ID
               return Response({'message': 'OTP successfully validated'}, status=status.HTTP_200_OK)
          else:
               return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
               


    

class Signout(APIView):
     # permission_classes = (IsAuthenticated, )
     def post(self, request):
          refresh_token = request.data.get('refresh_token')
          print(refresh_token)
          if refresh_token:
               try:
                    print('no')
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                    print('no')
                    response = JsonResponse({"message": "Logged out successfully."})
                
                    return response
               except:
                    return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
          else:
               return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)


