
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt  import views as jwt_views
from authentication.views import CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', 
          CustomTokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
    path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
    path('',include('authentication.urls'))
]
