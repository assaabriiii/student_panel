from rest_framework import serializers
from .models import Course, Exercise, Feedback, Comment, Announcement

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


class FeedbackSerializer(serializers.Serializer):
    ta = serializers.ReadOnlyField(source='ta.user.username')
    class Meta:
        model = Feedback
        fields = ['feedback_id', 'submission', 'feedback_text', 'grade', 'feedback_at']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.username')
    class Meta:
        model = Comment
        fields = ['comment_id', 'exercise', 'author', 'text', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    course = serializers.ReadOnlyField(source='course.code')
    class Meta:
        model = Announcement
        fields = ['announcement_id', 'author', 'course', 'title', 'body', 'created_at']
