from django.urls import path
from .views import *
urlpatterns = [
    path('userlist/', UserList.as_view(), name='user-list'),
    path('blockuser/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
    path('unblockuser/<int:user_id>/', UnblockUserView.as_view(), name='unblock-user'),
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('addcountry/', CountryCreateView.as_view(), name='add_country_api'),
    path('deletecountry/<int:country_id>/', CountryDeleteView.as_view(), name='country-delete'),
    path('add_course/', CourseCreateView.as_view(), name='create-course'),
    path('deletecourse/<int:course_id>/', CourseDeleteView.as_view(), name='course-delete'),



]
