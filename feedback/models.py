from django.db import models
from students.models import Student, Subject

class Exercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exercises')
    number_of_questions = models.PositiveIntegerField(default=0)
    deadline = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    mistakes = models.TextField()
    suggestions = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback for {self.student.university_number} - {self.exercise.title}"

class Comment(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='comments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.student.university_number} on {self.feedback}"

class Presence(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='presences')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='presences')
    date = models.DateField()
    present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marked_presences')  # TA who marked

    class Meta:
        unique_together = ('subject', 'student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.university_number} - {self.subject.name} on {self.date}: {'Present' if self.present else 'Absent'}"