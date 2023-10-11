from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userside.models import UserRequest  
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class UserRequestsForConsultancy(APIView):
    # permission_classes = [IsAuthenticated] 

    def get(self, request, user_id):
        # Retrieve the UserRequest objects for the specific consultancy (course)
        user_requests = UserRequest.objects.filter(course__added_by=user_id)

        # Serialize the user_requests queryset using your UserRequestSerializer
        serializer = UserRequestSerializer(user_requests, many=True)

        return Response({'user_requests': serializer.data}, status=status.HTTP_200_OK)
    
class ConsultantCourseListView(APIView):
    def get(self, request):
        # Retrieve all courses
        courses = Course.objects.all()
        
        # Serialize the course data
        serializer = CourseRequestSerializer(courses, many=True)
        
        # Return the serialized data as JSON response
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)
        
class ConsultantStudentList(APIView):
    def get(self, request, consultant_id):
        # Filter ConsultantRequest objects by consultant_id
        students = ConsultantRequest.objects.filter(consultant_id=consultant_id)
        
        # Serialize the students data
        serializer = ConsultantRequestSerializer(students, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditCourse(APIView):
    def post(self, request):
            # Parse incoming data
            course_id = request.data.get('courseId')
            print(course_id)
            updated_data = {
                'course': request.data.get('course'),
                'duration': request.data.get('duration'),
                'description': request.data.get('description'),
            }
            
            image=request.FILES.get('image') 
            print(image)        
               
        # try:
            # Fetch the Course object
            course = Course.objects.get(id=course_id)

            # Update the attributes of the Course object
            for attr, value in updated_data.items():
                setattr(course, attr, value)
            if image is not None:
                course.image=image
            # Save the updated Course object
            course.save()

            # Serialize the updated Course object
            # serializer = CourseSerializer(course)

            return Response( status=status.HTTP_200_OK)

        # except Course.DoesNotExist:
        #     return Response(
        #         {'error': 'Course not found'},
        #         status=status.HTTP_404_NOT_FOUND
        #     )
        # except Exception as e:
        #     return Response(
        #         {'error': str(e)},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )