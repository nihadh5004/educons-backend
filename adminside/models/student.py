from django.db import models
from  authentication.models  import CustomUser 
from .college import College
from .course import Course


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Add any additional fields related to students here
    # For example, you can add a field for student ID or GPA

    def __str__(self):
        return self.user.username  