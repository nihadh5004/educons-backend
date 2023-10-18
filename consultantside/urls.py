from django.urls import path
from .views import *
urlpatterns = [
    path('user-requests/<int:user_id>/', UserRequestsForConsultancy.as_view(), name='user_requests_for_consultancy'),
    path('consultant-courses/', ConsultantCourseListView.as_view(), name='consultant-course-list'),
    path('consultant-students/<int:consultant_id>/', ConsultantStudentList.as_view(), name='consultant-students'),
    path('edit-course/', EditCourse.as_view(), name='edit-course'),
    path('get-consultant-dashboard/<int:consultant_id>/', FetchConsultantDetails.as_view(), name='edit-course'),


]