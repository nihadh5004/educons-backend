
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_student =models.BooleanField(default=False)
    is_consultancy =models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    online= models.BooleanField(default=False)