from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, Feedback

@login_required
def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    feedback = Feedback.objects.filter(
        student=request.user,
        exercise=exercise
    ).first()
    
    return render(request, 'feedback/exercise_detail.html', {
        'exercise': exercise,
        'feedback': feedback
    })

@login_required
def exercise_list(request):
    exercises = Exercise.objects.all().order_by('-created_at')
    student_feedback = Feedback.objects.filter(student=request.user).values_list('exercise_id', flat=True)
    
    return render(request, 'feedback/exercise_list.html', {
        'exercises': exercises,
        'student_feedback': student_feedback
    })