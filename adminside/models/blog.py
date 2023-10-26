from django.db import models
from  authentication.models  import CustomUser 
 
 
   
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
    