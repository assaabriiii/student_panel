from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.StudentLoginView.as_view(), name='login'),
    path('logout/', views.Logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ta-dashboard/', views.ta_dashboard, name='ta_dashboard'),
    path('ta/attendance/<int:subject_id>/', views.mark_attendance, name='mark_attendance'),
    path('exercises/add/', views.add_exercise, name='add_exercise'),
    path('exercises/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),
]