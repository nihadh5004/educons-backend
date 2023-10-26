from django.db import models



class Country(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    advantages = models.TextField()
    cost_of_studying = models.TextField()
    image = models.ImageField(upload_to='country_images/', blank=True, null=True)

    def __str__(self):
        return self.name