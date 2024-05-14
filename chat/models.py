from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Change to ForeignKey
    slug = models.SlugField(max_length=100)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username  # Accessing username of the related User instance



class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', db_column='user_id')
    created_at = models.DateTimeField(default=timezone.now)  
    room = models.ForeignKey(Profile, on_delete=models.CASCADE)
