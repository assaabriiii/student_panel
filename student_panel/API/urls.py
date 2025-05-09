from django.urls import path
from .views import ExerciseCommentsView, StudentLastFiveExercisesView, StudentLoginView, StudentCoursesView, StudentExerciseView, StudentCurrExerciseView, StudentExerciseFeedbackView, StudentCourseExercisesView, StudentExercisesView, StudentCourseView, StudentAnnouncementsView, CreateAnnouncementView

urlpatterns = [
    path('student/login/', StudentLoginView.as_view(), name='student-login'),
    path('student/courses/', StudentCoursesView.as_view(), name='student-courses'),
    path('student/course/', StudentCourseView.as_view(), name='student-course'),
    path('student/exercises/', StudentCurrExerciseView.as_view(), name='student-exercises'),
    path('student/all/exercises/', StudentExercisesView.as_view(), name='student-all-exercises'),
    path('student/course/exercises/', StudentCourseExercisesView.as_view(), name='student-course-exercises'),
    path('student/exercise/feedback/', StudentExerciseFeedbackView.as_view(), name='student-exercise-feedback'),
    path('student/exercise/', StudentExerciseView.as_view(), name='student-exercise'),
    path('student/exercises/recent/', StudentLastFiveExercisesView.as_view(), name='student-last-five-exercises'),
    path('exercise/comments/', ExerciseCommentsView.as_view(), name='exercise-comments'),
    path('student/announcements/', StudentAnnouncementsView.as_view(), name='student-announcements'),
    path('announcement/create/', CreateAnnouncementView.as_view(), name='create-announcement')
    
]