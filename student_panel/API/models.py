from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.AutoField(primary_key=True)
    university_number = models.CharField(max_length=10, unique=True, default="0")
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrollment_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor_profile")
    professor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Prof. {self.name}"

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    semester = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(
        Student,
        through='Enrollment',
        related_name='enrolled_courses'
    )
    tas = models.ManyToManyField(
        Student,
        through='TAAssignment',
        related_name='ta_courses'
    )
    start_date = models.DateField(
        help_text="Date when this course begins",
    )
    end_date = models.DateField(
        help_text="Date when this course ends",
    )

    def __str__(self):
        return f"{self.code}: {self.title}"

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Session {self.session_id} of {self.course.code} on {self.date_time}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class TAAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_on = models.DateField(auto_now_add=True)
    role_desc = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"TA {self.student} for {self.course}"

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20)
    marked_by = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='marked_attendances'
    )
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'student')

    def clean(self):
        # Ensure marker is a TA for the session's course
        course = self.session.course
        if not TAAssignment.objects.filter(student=self.marked_by, course=course).exists():
            raise ValidationError('Marker must be a TA for this course')

    def __str__(self):
        return f"Attendance of {self.student} in {self.session} ({self.status})"

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exercises')
    created_by = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='created_exercises'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()

    def clean(self):
        # Ensure creator is a TA
        if not TAAssignment.objects.filter(student=self.created_by, course=self.course).exists():
            raise ValidationError('Only a TA of this course can create an exercise')

    def __str__(self):
        return f"{self.title} for {self.course.code}"

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Submission {self.submission_id} by {self.student}"

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='feedbacks')
    ta = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='given_feedbacks'
    )
    feedback_text = models.TextField(blank=True)
    grade = models.CharField(max_length=10, blank=True)
    feedback_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure that TA is assigned to the course of the exercise
        course = self.submission.exercise.course
        if not TAAssignment.objects.filter(student=self.ta, course=course).exists():
            raise ValidationError('Only a TA of this course can give feedback')

    def __str__(self):
        return f"Feedback by {self.ta} on submission {self.submission_id}"
