from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('list/', views.exercise_list, name='exercise_list'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('classes/<int:university_number>/', views.student_classes_with_ta, name='student_classes'),
    path('exercises/<int:university_number>/', views.latest_exercises_with_ta, name='latest_exercises'),
    path('create/<int:subject_id>/', views.create_feedback, name='create_feedback'),
    path('feedback/<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
    path('feedback/<int:feedback_id>/edit/', views.edit_feedback, name='edit_feedback'),
    path('feedback/<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),
    path('feedback/save/', views.save_feedback, name='save_feedback'),
]