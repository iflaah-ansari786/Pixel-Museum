from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Artwork(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='artworks/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title