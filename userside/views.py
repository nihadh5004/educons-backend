from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail , EmailMessage
from backend import settings
from rest_framework.permissions import IsAuthenticated
from authentication.custom_permission import IsAdmin
from authentication.models import *
from adminside.models.course import *
from .serializers import *
from adminside.serializers import *
from django.contrib.auth.models import User  # Import the User model from Django
class UserList(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self, request):
        # Query all users in the database
        users = CustomUser.objects.all()

        # Serialize the users data
        serializer = UserListSerializer(users, many=True)  # You should create a UserSerializer

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

class BlockUserView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def put(self, request, user_id):
        try:
            # Get the user by user_id
            user = CustomUser.objects.get(id=user_id)
            
            # Update the user's is_active status to False (blocking the user)
            user.is_active = False
            user.save()
            
            if user.is_consultancy:
                    subject = 'Account deactivated'
                    message = f'Hello {user.username},\nYour account has been de-activated,\n Now you cannot login with your username and password.'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

            
            return Response({'message': 'User blocked successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class UnblockUserView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def put(self, request, user_id):
        try:
            # Retrieve the user by ID
            user = CustomUser.objects.get(pk=user_id)

            # Check if the user is currently blocked
            if not user.is_active:
                # Unblock the user
                user.is_active = True
                user.save()
                # If you want to send an email when unblocking the user, uncomment the following code:
                if user.is_consultancy:
                    subject = 'Account activated'
                    message = f'Hello {user.username},\nYour account has been activated,\n Now you can login with your username and password.'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                # Return a success response
                return Response({"message": "User unblocked successfully"}, status=status.HTTP_200_OK)

            # Return a response indicating that the user is already active
            return Response({"message": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            # Return a response indicating that the user does not exist
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class CountryListView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountryInfoSerializer(countries, many=True)
        return Response(serializer.data)


class CountryCreateView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

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
        user_id = request.data.get('user_id')
        user=CustomUser.objects.get(id=user_id)
        print(user_id)
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
            is_active=is_active,
            added_by = user
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
        
from .models import *


class SubmitConsultantRequest(APIView):
    def post(self, request):
        # Retrieve data from the request
        consultant_id = request.data.get('userId')
        course_id = request.data.get('courseId')
        intake_year = request.data.get('intakeYear')
        intake_month = request.data.get('intakeMonth')
        username = request.data.get('username')
        
        user=CustomUser.objects.get(username=username)
        user_id=user.id
        try:
            # Create a new ConsultantRequest object
            consultant_request = ConsultantRequest.objects.create(
                user_id=user_id,
                course_id=course_id,
                intake_year=intake_year,
                intake_month=intake_month,
                consultant_id=consultant_id
            )

            # You can perform any additional actions here if needed

            # Return a success response
            return Response({'message': 'Consultant request submitted successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Return an error response if there's an exception
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from consultantside.serializers import ConsultantRequestSerializer  
        
class ConsultantRequestList(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self,request):
        requests=ConsultantRequest.objects.all()
        serializer = ConsultantRequestSerializer(requests, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ApproveConsultantRequest(APIView):
    def post(self, request, request_id):
        try:
            # Retrieve the consultant request by ID
            consultant_request = ConsultantRequest.objects.get(pk=request_id)
            user_id=consultant_request.user.id
            user=CustomUser.objects.get(pk=user_id)
            user.is_student=True
            user.save()
            # Approve the request by setting is_approved to True
            consultant_request.is_approved = True
            consultant_request.save()

            # You can perform any additional actions here if needed

            # Return a success response
            return Response({'message': 'Consultant request approved successfully.'}, status=status.HTTP_200_OK)
        except ConsultantRequest.DoesNotExist:
            # Return a not found response if the request ID is invalid
            return Response({'error': 'Consultant request not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Return an error response if there's an exception
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class CourseBlockView(APIView):
    def post(self, request):
        course_id = request.data.get('courseId')
        try:
            # Retrieve the course by ID
            course = Course.objects.get(pk=course_id)
            
            # Toggle the is_active status (block if unblocked, unblock if blocked)
            course.is_active = not course.is_active
            course.save()
            
            # Return a success response with the updated is_active status
            response_data = {
                'message': 'Course status updated successfully.',
                'is_active': course.is_active,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            # Return a not found response if the course ID is invalid
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Return an error response if there's an exception
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class FetchAdminDetails(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self,request):
        try:
            students=CustomUser.objects.filter(is_student=True).count()
            courses=Course.objects.all().count()
            users=CustomUser.objects.filter(is_consultancy=False,is_superuser=False).count()
            requests=ConsultantRequest.objects.filter(is_approved = False).count()
            userlist=CustomUser.objects.filter(is_consultancy=False,is_superuser=False).order_by('-id')[:3]
            
            serializer = UserListSerializer(userlist, many=True)
            data = {
                "students": students,
                "pendings": requests,
                "users": users,
                "courses": courses,
                "userlist": serializer.data  # Add serialized userlist to the response
            }

                # Return the data in the response
            return Response(data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            # Handle the case where the consultant is not found
            return Response({"error": "Consultant not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
