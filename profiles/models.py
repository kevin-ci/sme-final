from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField
from companies.models import Company

# Create your models here.


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, null=True, blank=True)
    headline = models.CharField(max_length=50, null=True, blank=True)
    profile_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.user.email


class Connection(models.Model):
    from_user = models.ForeignKey(
        UserProfile, related_name='connections', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        UserProfile, related_name='connected_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def connection_exists(user_profile_a, user_profile_b):
        return Connection.objects.filter(
            (models.Q(from_user=user_profile_a) & models.Q(to_user=user_profile_b)) |
            (models.Q(from_user=user_profile_b) & models.Q(to_user=user_profile_a))
        ).exists()
        
    @staticmethod
    def get_connection(user_profile_a, user_profile_b):
        return Connection.objects.filter(
            (models.Q(from_user=user_profile_a) & models.Q(to_user=user_profile_b)) |
            (models.Q(from_user=user_profile_b) & models.Q(to_user=user_profile_a))
        )
        
class Job(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='jobs')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()