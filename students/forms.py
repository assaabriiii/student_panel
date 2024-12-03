from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Student

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='University Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your university number'
        })
    )
    # Remove password field
    password = None

    def clean(self):
        university_number = self.cleaned_data.get('username')
        if university_number:
            try:
                student = Student.objects.get(university_number=university_number)
                self.user_cache = student
            except Student.DoesNotExist:
                raise forms.ValidationError('Invalid university number.')
        return self.cleaned_data
