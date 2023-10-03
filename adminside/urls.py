from django.urls import path
from .views import *
urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('filterview/', FilterlistView.as_view(), name='course-list'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('course-details/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('postcomment/' , CommentView.as_view(), name='post-comment'),
    path('bloglikes/' , BlogLikeView.as_view(), name='post-comment'),
    path('blogsave/' , SaveBlogView.as_view(), name='post-comment'),
    path('checksave/', CheckSaveView.as_view(), name='check_save_view'),
    path('submit-blog/', BlogCreateView.as_view(), name='submit-blog'),
    path('update-profile/<int:profile_id>/', UpdateProfileView.as_view(), name='update-profile'),

]
