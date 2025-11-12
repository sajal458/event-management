from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# class UserProfile(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='userprofile')
#     profile_image=models.ImageField(upload_to='profile_image',blank=True)
#     phone_number = models.CharField(max_length=15,blank=True)
#     def __str__(self):
#         return f"{self.user.username}"
    
class CustomUser(AbstractUser):
    profile_image=models.ImageField(upload_to='profile_image',blank=True,default='profile_image/defualt_pro.jpg')
    phone_number = models.CharField(max_length=15,blank=True)
    def __str__(self):
        return self.username