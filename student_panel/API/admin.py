from django.contrib import admin
from .models import Announcement, Comment, Student, Professor, Course, Subject, Session, Enrollment, TAAssignment, Attendance, Exercise, Submission, Feedback

admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Session)
admin.site.register(Enrollment)
admin.site.register(TAAssignment)
admin.site.register(Attendance)
admin.site.register(Exercise)
admin.site.register(Submission)
admin.site.register(Feedback)
admin.site.register(Comment)
admin.site.register(Announcement)