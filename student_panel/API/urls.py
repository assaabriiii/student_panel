from django.urls import path
from .views import StudentLoginView, StudentCoursesView

urlpatterns = [
    path('student/login/', StudentLoginView.as_view(), name='student-login'),
    path('student/courses/', StudentCoursesView.as_view(), name='student-courses'),
]