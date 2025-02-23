from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, Feedback, Comment
from django.http import JsonResponse

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
    exercises = Exercise.objects.all().order_by('-created_at')
    student_feedback = Feedback.objects.filter(student=request.user).values_list('exercise_id', flat=True)
    
    return render(request, 'feedback/exercise_list.html', {
        'exercises': exercises,
        'student_feedback': student_feedback
    })