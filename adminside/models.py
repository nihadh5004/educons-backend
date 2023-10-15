from django.db import models
from  authentication.models  import CustomUser
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    advantages = models.TextField()
    cost_of_studying = models.TextField()
    image = models.ImageField(upload_to='country_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class College(models.Model):
    name = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class CourseType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


from django.utils import timezone

class Course(models.Model):
    name = models.CharField(max_length=200)
    college = models.ForeignKey('College', on_delete=models.CASCADE)
    course_type = models.ForeignKey('CourseType', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in Years")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    
    def __str__(self):
        return self.name
    
class Blog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_blogs', blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.heading
    
class BlogComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who made the comment
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)  # Blog that the comment belongs to
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on '{self.blog.heading}'"
    
    
   
class CommentReply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who made the comment
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE)  # Blog that the comment belongs to
    reply = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on '{self.comment.comment}'"
    
class BlogLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who liked the blog
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)  # Blog that was liked
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on '{self.blog.heading}'"
    
class SavedBlog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'blog']

    def __str__(self):
        return f"{self.user.username} saved '{self.blog.heading}' "
    
    

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Add any additional fields related to students here
    # For example, you can add a field for student ID or GPA

    def __str__(self):
        return self.user.username  