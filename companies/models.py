from django.db import models

# Create your models here.
class Company(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name