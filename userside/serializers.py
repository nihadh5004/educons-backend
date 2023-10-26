from rest_framework import serializers
from authentication.models import CustomUser
from adminside.models.country import *
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','phone','is_active', 'date_joined' , 'is_student' , 'is_consultancy']  # Add any other fields you want to include

class CountryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name'] 