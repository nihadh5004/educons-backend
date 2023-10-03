from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer 

# Create your views here.


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            username = request.query_params.get('username')
            print(username )
            user=CustomUser.objects.get(username=username)
            print(user)
            # Check if the user exists
            if not user:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomUserSerializer(user)
            print('yes')

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)