from rest_framework import serializers
from .models import *
from authentication.models import CustomUser


class ConsultancySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username','phone')

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'


class CollegeSerializer(serializers.ModelSerializer):
    country = CountrySerializer()  # Serialize the Country model

    class Meta:
        model = College
        fields = '__all__'
        


class CourseSerializer(serializers.ModelSerializer):
    college = CollegeSerializer()  # Serialize the Country model
    course_type = CourseTypeSerializer()  # Serialize the CourseType model
    added_by=ConsultancySerializer()
    class Meta:
        model = Course
        fields = ['id', 'name', 'college',  'course_type', 'description', 'duration', 'is_active', 'image', 'added_by']

class TruncatedContentField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1000  # Set an arbitrary max_length
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        words = value.split()[:20]  # Truncate to 12 words
        truncated_content = ' '.join(words)
        return truncated_content


class BlogSerializer(serializers.ModelSerializer):
    truncated_content = TruncatedContentField(source='content', read_only=True)
    username = serializers.ReadOnlyField(source='user.username') 
    class Meta:
        model = Blog
        fields = ('id', 'username', 'heading', 'image', 'truncated_content', 'created_date', 'is_active')
        
        
class BlogDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username') 
    class Meta:
        model = Blog
        fields = ('id', 'username', 'heading', 'image', 'content', 'created_date','is_active')
        
        


class BlogCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogComment
        fields = '__all__' 