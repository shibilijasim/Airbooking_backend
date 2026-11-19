from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    APPROVAL_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default='Pending'
    )