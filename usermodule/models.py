from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    objects = None
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    otp = models.CharField(max_length=6, default=None, null=True)

    class Meta:
        db_table = "users"

