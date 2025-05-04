from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Student
from feedback.models import Exercise

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


class ExerciseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        ta_subjects = kwargs.pop('ta_subjects', None)
        super().__init__(*args, **kwargs)
        if ta_subjects is not None:
            self.fields['subject'].queryset = ta_subjects
    class Meta:
        model = Exercise
        fields = ['title', 'description', 'subject', 'number_of_questions']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }