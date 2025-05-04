from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, Feedback, Comment
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

@login_required
def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    feedback = Feedback.objects.filter(
        student=request.user,
        exercise=exercise
    ).first()
    
    if request.method == 'POST' and feedback:
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(
                feedback=feedback,
                student=request.user,
                text=comment_text
            )
            messages.success(request, 'Comment added successfully.')
            return redirect('exercise_detail', exercise_id=exercise_id)
    
    # Get all comments for this exercise across all feedbacks
    all_comments = Comment.objects.filter(
        feedback__exercise=exercise
    ).select_related('student', 'feedback').order_by('created_at')
    
    return render(request, 'feedback/exercise_detail.html', {
        'exercise': exercise,
        'feedback': feedback,
        'comments': all_comments
    })

@login_required
def exercise_list(request):
    user = request.user
    # Only show exercises for subjects the student is enrolled in
    subjects = user.subjects.all() if hasattr(user, 'subjects') else []
    exercises = Exercise.objects.filter(subject__in=subjects).order_by('-created_at')
    student_feedback = Feedback.objects.filter(student=user).values_list('exercise_id', flat=True)
    
    return render(request, 'feedback/exercise_list.html', {
        'exercises': exercises,
        'student_feedback': student_feedback
    })

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.student != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('exercise_detail', exercise_id=comment.feedback.exercise.id)
    return render(request, 'feedback/edit_comment.html', {'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.student != request.user:
        return HttpResponseForbidden()
    exercise_id = comment.feedback.exercise.id
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('exercise_detail', exercise_id=exercise_id)
    return render(request, 'feedback/delete_comment.html', {'comment': comment})

@login_required
@require_POST
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    feedback = parent_comment.feedback
    reply_text = request.POST.get('reply')
    if reply_text:
        Comment.objects.create(
            feedback=feedback,
            student=request.user,
            text=reply_text,
            parent=parent_comment
        )
        messages.success(request, 'Reply added successfully.')
    return redirect('exercise_detail', exercise_id=feedback.exercise.id)