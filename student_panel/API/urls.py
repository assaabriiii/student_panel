from django.urls import path
from .views import StudentLoginView, StudentCoursesView, StudentExerciseView, StudentCurrExerciseView

urlpatterns = [
    path('student/login/', StudentLoginView.as_view(), name='student-login'),
    path('student/courses/', StudentCoursesView.as_view(), name='student-courses'),
    path('student/exercises/', StudentCurrExerciseView.as_view(), name='student-exercises'),
    path('student/all/exercises/', StudentExerciseView.as_view(), name='student-all-exercises'),
]