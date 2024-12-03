from django.urls import path
from . import views

urlpatterns = [
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('list/', views.exercise_list, name='exercise_list'),
]