from rest_framework import serializers
from userside.models import *
from adminside.serializers import CourseSerializer
from authentication.models import *
from authentication.serializers import *
from adminside.serializers import CollegeSerializer

class CourseRequestSerializer(serializers.ModelSerializer):
    college = CollegeSerializer() 
    class Meta:
        model = Course
        fields = ['id', 'name', 'college',  'added_by']

class UserRequestSerializer(serializers.ModelSerializer):
    user=CustomUserSerializer()
    course=CourseRequestSerializer()
    class Meta:
        model = UserRequest
        fields = ['id','user','course']  
        
class ConsultantRequestSerializer(serializers.ModelSerializer):
    user=CustomUserSerializer()
    consultant=CustomUserSerializer()
    course=CourseRequestSerializer()
    class Meta:
        model = ConsultantRequest
        fields = ['id','user','course','intake_year','intake_month', 'consultant' , 'is_approved']  