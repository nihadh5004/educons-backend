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
    # permission_classes = [IsAuthenticated]

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
        
class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        username = request.data.get('username')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if uploaded_file:
            user.image = uploaded_file
            user.save()
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)