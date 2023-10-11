from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from authentication.serializers import CustomUserSerializer 

# Create your views here.
class CourseListView(APIView):
    def get(self, request):
        try:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching courses."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class ConsultancyCourseList(APIView):
    def get(self, request,user_id):
        # try:
            courses = Course.objects.filter(added_by=user_id)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response(
        #         {"error": "An error occurred while fetching courses."},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

class CourseDetailView(APIView):
    def get (self,request , course_id):
        try:
            course=get_object_or_404(Course, pk=course_id)
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching the course."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
             
class FilterlistView(APIView):
    def get(self,request):
        # try:
            countries = Country.objects.all()
            coursetype = CourseType.objects.all()
            colleges = College.objects.all()
            consultancies=CustomUser.objects.filter(is_consultancy=True)
            
            collegeserializer = CollegeSerializer(colleges, many=True)
            countryserializer = CountrySerializer(countries, many=True)
            coursetypeserializer = CourseTypeSerializer(coursetype, many=True)
            consultancyserializer = ConsultancySerializer(consultancies, many=True)
            response_data = {
                "collegesData": collegeserializer.data,
                "countriesData": countryserializer.data,
                "coursetypeData": coursetypeserializer.data,
                "ConsultanciesData": consultancyserializer.data ,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response(
        #         {"error": "An error occurred while fetching data."},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
            
class BlogListView(APIView):
    def get(self, request):
        # try:
            blogs = Blog.objects.all()
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response(
        #         {"error": "An error occurred while fetching blogs."},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
        
class BlogDetailView(APIView):
    def get(self, request, blog_id):
        try:
            blog = get_object_or_404(Blog, pk=blog_id)
            serializer = BlogDetailSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching the blog."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BlogBlockView(APIView):
    def post(self, request, blog_id):
        try:
            blog = get_object_or_404(Blog, pk=blog_id)
            # Check the current state of the blog and toggle it
            blog.is_active = not blog.is_active
            blog.save()
            serializer = BlogDetailSerializer(blog)
            
            # Determine the response message based on the current state
            if blog.is_active:
                message = "Blog unblocked successfully."
            else:
                message = "Blog blocked successfully."

            return Response({"message": message, "blog_data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while updating the blog state."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
            
class CommentView(APIView):
    def post(self, request):
        blog_id = request.data.get('blogId')
        username = request.data.get('username')
        comment_text = request.data.get('comment')

        try:
            user = CustomUser.objects.get(username=username)
            blog = Blog.objects.get(pk=blog_id)

            blog_comment = BlogComment.objects.create(user=user, blog=blog, comment=comment_text)

            # Serialize the newly created comment
            serializer = BlogCommentSerializer(blog_comment)

            # Include 'user_id' and 'username' in the response data
            response_data = {
                **serializer.data,
                "username": user.username,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while posting comment."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def get(self, request):
        blog_id = request.query_params.get('blogId')  # Retrieve blogId from query parameters
        try:
            blog = Blog.objects.get(pk=blog_id)
            comments = BlogComment.objects.filter(blog=blog)
            comment_data = []

            for comment in comments:
                comment_data.append({
                    'id': comment.id,
                    'user': comment.user.id,
                    'username': comment.user.username,
                    'comment': comment.comment,
                    'blog' : blog.id,
                    'created_date': comment.created_date
                })

            return Response(comment_data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching comments."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )






class BlogLikeView(APIView):
    def post(self, request):
        blog_id = request.data.get('blogId')
        username=request.data.get('username')  # Assuming you have authentication set up
        
        try:
            user=CustomUser.objects.get(username=username)
            blog = Blog.objects.get(pk=blog_id)

       
            # Check if the user has already liked the blog post
            existing_like = BlogLike.objects.filter(user=user, blog=blog).first()

            if existing_like:
                existing_like.delete()  # Delete the like object if it exists
                return Response({'message': 'You have unliked this blog post.'}, status=status.HTTP_200_OK)

            # Create a new BlogLike instance to represent the like
            like = BlogLike(user=user, blog=blog)
            like.save()

            # Optionally, you can return the updated number of likes for the blog post
            likes_count = BlogLike.objects.filter(blog=blog).count()
            return Response({'message': 'Blog post liked', 'likes_count': likes_count }, status=status.HTTP_201_CREATED)

        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while posting like."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def get(self, request):
        try:
            blog_id = request.query_params.get('blogId')
            blog = Blog.objects.get(pk=blog_id)
            username = request.query_params.get('username')  # Get the username from query parameters
            
            # Count the total likes for the blog post
            likes_count = BlogLike.objects.filter(blog=blog).count()
            
            # Check if the current user (identified by the provided username) has liked the blog post
            user_liked = False
            if username:
                user = CustomUser.objects.get(username=username)
                user_liked = BlogLike.objects.filter(blog=blog, user=user).exists()
            
            return Response({
                'likesCount': likes_count,
                'userLiked': user_liked,
            }, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching likes count."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class SaveBlogView(APIView):
    def post(self, request):
        blog_id = request.data.get('blogId')
        username = request.data.get('username')  
        
        try:
            user = CustomUser.objects.get(username=username)
            blog = get_object_or_404(Blog, pk=blog_id)

            # Check if the user has already saved the blog
            saved_blog = SavedBlog.objects.filter(user=user, blog=blog).first()
            if saved_blog:
                # If it exists, delete the saved blog
                saved_blog.delete()
                return Response({'message': 'Blog removed from saved blogs'}, status=status.HTTP_200_OK)

            # If it doesn't exist, create a new SavedBlog instance to represent the saved blog
            saved_blog = SavedBlog(user=user, blog=blog)
            saved_blog.save()

            return Response({'message': 'Blog saved successfully'}, status=status.HTTP_201_CREATED)

        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while saving the blog."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class CheckSaveView(APIView):
    def get(self, request):
        # Get the blog ID and username from the query parameters
        blog_id = request.query_params.get('blogId')
        username = request.query_params.get('username')

        try:
            user = CustomUser.objects.get(username=username)
            blog = Blog.objects.get(pk=blog_id)

            # Check if the user has saved the blog
            is_saved = SavedBlog.objects.filter(user=user, blog=blog).exists()

            return Response({'isSaved': is_saved}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while checking if the blog is saved."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class BlogCreateView(APIView):
    def post(self, request, format=None):
        # Get data from the request
        heading = request.data.get('heading')
        image = request.data.get('image')
        content = request.data.get('content')
        username = request.data.get('username')  # Assuming you send the username from the frontend

        try:
            # Get the user object by username
            user = CustomUser.objects.get(username=username)

            # Create a new Blog object with user, heading, image, and content
            blog = Blog(user=user, heading=heading, image=image, content=content)

            # Save the Blog object
            blog.save()

            # Return a response indicating success
            return Response({'message': 'Blog created successfully'}, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            # Return a response indicating the user was not found
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Return a response indicating an error occurred
            return Response({'error': 'An error occurred while creating the blog'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class UpdateProfileView(APIView):
    def put(self, request, profile_id, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        contact = request.data.get('contact')
        
        try:
            user = CustomUser.objects.get(id=profile_id)
            
            # Check if the requested username already exists (excluding the current user)
            if CustomUser.objects.filter(username=username).exclude(id=profile_id).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's profile data
            user.username = username
            user.phone = contact
            user.email = email
            user.save()
            
            serializer = CustomUserSerializer(user)
            print('yes')

            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
 
from userside.models import UserRequest
       
class CreateUserRequest(APIView):
    def post(self, request, format=None):
        # Get user ID and course ID from the request data
        user_id = request.data.get('user')
        course_id = request.data.get('course')

        try:
            # Check if the UserRequest already exists for the given user and course
            existing_request = UserRequest.objects.filter(user_id=user_id, course_id=course_id).first()

            if existing_request:
                return Response({'detail': 'UserRequest already exists for this user and course.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new UserRequest
            user_request = UserRequest.objects.create(user_id=user_id, course_id=course_id)
            user_request.save()

            return Response({'detail': 'UserRequest created successfully.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class StudentsList(APIView):
    def get(self,request):
        students = CustomUser.objects.filter(is_student=True)
        
        serializer = CustomUserSerializer(students, many=True)
        print('yes')

        return Response(serializer.data, status=status.HTTP_200_OK)
