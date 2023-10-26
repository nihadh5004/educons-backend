from django.db import models
from  authentication.models  import CustomUser


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