from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import *
from adminside.models import *
from .serializers import *
from adminside.serializers import *
from django.contrib.auth.models import User  # Import the User model from Django
class UserList(APIView):
    def get(self, request):
        # Query all users in the database
        users = CustomUser.objects.all()

        # Serialize the users data
        serializer = UserListSerializer(users, many=True)  # You should create a UserSerializer

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

class BlockUserView(APIView):
    def put(self, request, user_id):
        try:
            # Get the user by user_id
            user = CustomUser.objects.get(id=user_id)
            
            # Update the user's is_active status to False (blocking the user)
            user.is_active = False
            user.save()
            
            return Response({'message': 'User blocked successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class UnblockUserView(APIView):
    def put(self, request, user_id):
        try:
            # Retrieve the user by ID
            user = CustomUser.objects.get(pk=user_id)

            # Check if the user is currently blocked
            if not user.is_active:
                # Unblock the user
                user.is_active = True
                user.save()

                # Return a success response
                return Response({"message": "User unblocked successfully"}, status=status.HTTP_200_OK)

            # Return a response indicating that the user is already active
            return Response({"message": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            # Return a response indicating that the user does not exist
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class CountryListView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountryInfoSerializer(countries, many=True)
        return Response(serializer.data)


class CountryCreateView(APIView):
    def post(self, request, format=None):
        # Get all the data from the request
        name = request.data.get('name')
        about = request.data.get('about')
        description = request.data.get('description')
        advantages = request.data.get('advantages')
        image = request.data.get('image')

        # Create a new Country object
        country = Country(
            name=name,
            about=about,
            cost_of_studying=description,
            advantages=advantages,
            image=image
        )

        # Save the object to the database
        country.save()

        # Return a response indicating success
        return Response({'message': 'Country created successfully'}, status=status.HTTP_201_CREATED)
    
    
class CountryDeleteView(APIView):
    def delete(self, request, country_id, format=None):
        try:
            # Retrieve the country object to delete
            country = Country.objects.get(pk=country_id)
            
            # Delete the country object
            country.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Country.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class CourseCreateView(APIView):
    def post(self, request, format=None):
        # Get all the data from the request
        print('hello')
        name = request.data.get('name')
        college_id = request.data.get('college')
        
        print(college_id)
        course_type_id = request.data.get('course_type')
        print(course_type_id)
        image = request.data.get('image')
        duration = request.data.get('duration')
        description = request.data.get('description')
        is_active = request.data.get('is_active')
        if is_active == 'true':
            is_active = True
        else:
            is_active = False
        # Create a new Course object
        course = Course(
            name=name,
            college_id=college_id,
            course_type_id=course_type_id,
            image=image,
            duration=duration,
            description=description,
            is_active=is_active
        )

        # Save the object to the database
        course.save()

        # Return a response indicating success
        return Response({'message': 'Course created successfully'}, status=status.HTTP_201_CREATED)
    
class CourseDeleteView(APIView):
    def delete(self, request, course_id, format=None):
        try:
            # Retrieve the course instance by its ID
            course = Course.objects.get(id=course_id)
            # Delete the course
            course.delete()
            return Response({'message': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)