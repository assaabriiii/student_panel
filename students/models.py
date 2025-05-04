from django.contrib.auth.models import AbstractUser
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE, related_name='subjects')
    students = models.ManyToManyField('Student', related_name='subjects')
    # number_of_questions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Professor(models.Model):
    user = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='professor_profile')
    # Add more professor-specific fields as needed

    def __str__(self):
        return f"Professor {self.user.get_full_name()}"

class Student(AbstractUser):
    university_number = models.CharField(max_length=20, unique=True)
    is_ta = models.BooleanField(default=False)
    ta_subjects = models.ManyToManyField('Subject', related_name='tas', blank=True)
    # is_ta: can be both TA and student if checked

    USERNAME_FIELD = 'university_number'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.university_number} - {self.get_full_name()}"

    def save(self, *args, **kwargs):
        self.set_unusable_password()
        super().save(*args, **kwargs)
