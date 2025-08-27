from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
import string
import random

class UserManager(BaseUserManager):
    """Custom user manager that uses username as primary identifier"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('full_name', 'Super Admin')
        extra_fields.setdefault('contact', '0000000000')
        extra_fields.setdefault('company', 'Admin')
        extra_fields.setdefault('address', 'Admin Address')
        extra_fields.setdefault('industry', 'Admin')
        
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    """Custom User Model with additional fields"""
    
    # Keep username field as required by specifications
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, db_index=True)
    
    # Additional required fields
    full_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=20, unique=True)
    company = models.CharField(max_length=255)
    address = models.TextField()
    industry = models.CharField(max_length=100)
    
    # Auto-generated unique user ID
    user_id = models.CharField(max_length=10, unique=True, editable=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'  # Use username as primary identifier
    REQUIRED_FIELDS = ['email', 'full_name', 'contact', 'company']
    
    objects = UserManager()  # Use custom manager
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_unique_user_id()
        super().save(*args, **kwargs)
    
    def generate_unique_user_id(self):
        """Generate a unique 10-character user ID"""
        while True:
            # Generate random 10-character ID with letters and numbers
            user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not User.objects.filter(user_id=user_id).exists():
                return user_id
    
    def __str__(self):
        return f"{self.full_name} ({self.user_id})"
