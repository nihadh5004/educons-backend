
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt  import views as jwt_views
from authentication.views import CustomTokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', 
          CustomTokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
    path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
    path('',include('authentication.urls')),
    path('',include('profileapp.urls')),
    path('',include('adminside.urls')),
    path('',include('userside.urls')),
    path('',include('consultantside.urls')),
    path('',include('chat.urls')),
    path('api/stripe/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)