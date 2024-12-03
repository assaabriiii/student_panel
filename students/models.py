from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    university_number = models.CharField(max_length=20, unique=True)
    
    USERNAME_FIELD = 'university_number'
    REQUIRED_FIELDS = ['username', 'email']
    
    def __str__(self):
        return f"{self.university_number} - {self.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Set an unusable password since we don't use password authentication
        self.set_unusable_password()
        super().save(*args, **kwargs)
