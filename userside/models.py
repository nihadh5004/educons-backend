from django.db import models
from authentication.models import CustomUser
from adminside.models.course import Course
# Create your models here.
class UserRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.user.username} for {self.course.name}"
    
    

class ConsultantRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    intake_year = models.CharField(max_length=100)
    intake_month = models.CharField(max_length=100)
    consultant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consultant_requests')
    is_approved = models.BooleanField(default=False)  # Default value set to False

    def __str__(self):
        return f"Consultant Request for {self.course.name} by {self.user.username}"