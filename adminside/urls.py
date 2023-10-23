from django.urls import path
from .views import *
urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('top-courses/', TopCourses.as_view(), name='top-course-list'),
    path('consultancy-courses/<int:user_id>/', ConsultancyCourseList.as_view(), name='course-list'),
    path('filterview/', FilterlistView.as_view(), name='course-list'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('block-blog/<int:blog_id>/', BlogBlockView.as_view(), name='block-blog'),
    path('course-details/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('postcomment/' , CommentView.as_view(), name='post-comment'),
    path('reply/' , CommentReplyCreate.as_view(), name='reply'),
    path('bloglikes/' , BlogLikeView.as_view(), name='post-comment'),
    path('blogsave/' , SaveBlogView.as_view(), name='post-comment'),
    path('checksave/', CheckSaveView.as_view(), name='check_save_view'),
    path('submit-blog/', BlogCreateView.as_view(), name='submit-blog'),
    path('update-profile/<int:profile_id>/', UpdateProfileView.as_view(), name='update-profile'),
    path('create-user-request/', CreateUserRequest.as_view(), name='create-user-request'),
    path('student-chat-list/', StudentsList.as_view(), name='student-chat-list'),

]
