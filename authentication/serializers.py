from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['is_superuser'] = user.is_superuser
        data['is_student'] = user.is_student
        data['is_consultancy'] = user.is_consultancy
        data['is_premium'] = user.is_premium
        data['id']=user.id
        return data





class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'image','is_student')


