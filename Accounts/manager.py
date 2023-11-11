from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,phone_number,password=None,**extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        if not email : 
            raise ValueError("email is required")
        
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',False)
        
        user=self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        
        return user
    
    def create_superuser(self,email,phone_number,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        return self.create_user(email,phone_number,password,**extra_fields)
        
        