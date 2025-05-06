from rest_framework import serializers
from students.models import Student
from feedback.models import Feedback, Exercise, Subject

class UniversityNumberLoginSerializer(serializers.Serializer):
    university_number = serializers.CharField()
    class Meta:
        model = Student
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class ExerciseSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'description', 'created_at', 'subject', 'number_of_questions', 'deadline']

class FeedbackSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()
    class Meta:
        model = Feedback
        fields = ['id', 'exercise', 'mistakes', 'suggestions', 'score', 'created_at']

class MarkAttendanceSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()

    class AttendanceRecordSerializer(serializers.Serializer):
        student_id = serializers.IntegerField()
        present = serializers.BooleanField()

    attendance = serializers.ListField(child=AttendanceRecordSerializer())

    class Meta:
        fields = ['subject_id', 'attendance']
