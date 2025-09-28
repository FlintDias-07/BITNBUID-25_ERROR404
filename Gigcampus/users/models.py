from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    ]
    
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    rating = models.FloatField(default=0.0)
    bio = models.TextField(blank=True, null=True)
    
    # Notification Preferences
    email_projects = models.BooleanField(default=True)
    email_bids = models.BooleanField(default=True)
    email_messages = models.BooleanField(default=True)
    email_payments = models.BooleanField(default=False)
    push_messages = models.BooleanField(default=True)
    push_bids = models.BooleanField(default=False)
    
    # Platform Preferences
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    profile_public = models.BooleanField(default=True)
    show_online_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"