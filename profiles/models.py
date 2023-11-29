from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, null=True, blank=True)
    heading = models.CharField(max_length=50, null=True, blank=True)
    profile_image = CloudinaryField('image', default='placeholder')
    
    def __str__(self):
        return self.user.email