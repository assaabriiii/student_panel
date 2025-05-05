from django import forms
from .models import Feedback, Exercise
from students.models import Student

class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, subject=None, **kwargs):
        super().__init__(*args, **kwargs)
        if subject is not None:
            self.fields['student'].queryset = Student.objects.filter(subjects=subject)
            self.fields['exercise'].queryset = Exercise.objects.filter(subject=subject)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    class Meta:
        model = Feedback
        fields = ['student', 'exercise', 'mistakes', 'score']
        widgets = {
            'mistakes': forms.Textarea(attrs={'rows': 3}),
            'score': forms.NumberInput(attrs={'step': '0.01'})
        }