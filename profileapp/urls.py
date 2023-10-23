from django.urls import path
from .views import *
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('upload-profile-pic/', FileUploadView.as_view(), name='profile'),
    path('saved-blogs/<int:user_id>/', SavedBlogs.as_view(), name='saved-blogs'),

]
