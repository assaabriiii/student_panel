from django.urls import path
from . import views

urlpatterns = [
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('list/', views.exercise_list, name='exercise_list'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
]