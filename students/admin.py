from django.contrib import admin
from .models import Student, Professor, Subject


admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Professor)

