from rest_framework import serializers
from .models import Course, Exercise

class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'code', 'title', 'semester']


class ExerciseSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.user.username')
    class Meta:
        model = Exercise
        fields = ['course', 'exercise_id', 'title', 'description', 'due_date', 'created_by']