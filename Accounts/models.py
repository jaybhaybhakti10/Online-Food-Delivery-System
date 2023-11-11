from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import UserManager


# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    
    username=None
    phone_number=models.CharField(max_length=10,unique=True,null=False)
    email=models.EmailField(unique=True,null=False,max_length=100)
    
    is_staff=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['phone_number']
    
    objects=UserManager()
    class Meta:
        verbose_name= 'User'