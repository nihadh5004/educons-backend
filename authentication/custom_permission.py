from rest_framework import permissions
from authentication.models import CustomUser 
from chat.views import get_user_from_token
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

def get_access_token(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    
    if not authorization_header:
        raise AuthenticationFailed("Authorization header is missing")
    
    try:
        _, access_token = authorization_header.split(' ')
        return access_token
    except ValueError:
        raise AuthenticationFailed("Invalid authorization header format")

def get_user_from_token(token_key):
    try:
        decoded_token = AccessToken(token_key)
        user_id = decoded_token['user_id']
        return user_id
    except:
        return None
    
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        access_token = get_access_token(request)

        if access_token:
            user_id = get_user_from_token(access_token)
            user = CustomUser.objects.filter(id=user_id, is_superuser=True).first()
            if user:
                return True  # The user is an admin
        return False  # Access is denied
    
class IsConsultant(permissions.BasePermission):
    def has_permission(self, request, view):
        access_token = get_access_token(request)

        if access_token:
            user_id = get_user_from_token(access_token)
            user = CustomUser.objects.filter(id=user_id, is_consultancy=True).first()
            if user:
                return True  # The user is an admin
        return False  # Access is denied