from django.contrib import admin
from .models import Exercise, Feedback, Comment, Presence 

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'exercise', 'score', 'created_at')
    list_filter = ('exercise', 'created_at')
    search_fields = ('student__university_number', 'exercise__title')


admin.site.register(Comment)
admin.site.register(Presence)