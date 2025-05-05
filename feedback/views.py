from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, Feedback, Comment
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from students.models import Student, Subject

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


def student_classes_with_ta(request, university_number):
    """
    Returns JSON response with subjects (classes) the student is enrolled in that have at least one TA.
    """
    student = Student.objects.filter(university_number=university_number).first()
    if not student:
        return JsonResponse({'error': 'Student not found'}, status=404)
    # Subjects the student is in, and that have at least one TA
    subjects = Subject.objects.filter(students=student, tas__isnull=False).distinct()
    data = [{'id': s.id, 'name': s.name} for s in subjects]
    return JsonResponse({'subjects': data})

def latest_exercises_with_ta(request, university_number):
    """
    Returns JSON response with the 5 latest exercises (by deadline) for subjects the student is in, where the subject has a TA.
    """
    student = Student.objects.filter(university_number=university_number).first()
    if not student:
        return JsonResponse({'error': 'Student not found'}, status=404)
    subjects = Subject.objects.filter(students=student, tas__isnull=False).distinct()
    exercises = Exercise.objects.filter(subject__in=subjects, deadline__isnull=False).order_by('-deadline')[:5]
    data = [{
        'id': e.id,
        'title': e.title,
        'subject': e.subject.name,
        'deadline': e.deadline,
        'description': e.description
    } for e in exercises]
    return JsonResponse({'exercises': data})