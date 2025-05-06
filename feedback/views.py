from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, Feedback, Comment
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from students.models import Student, Subject
from .forms import FeedbackForm
from .models import Subject

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


@login_required
def create_feedback(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, subject=subject)
        if form.is_valid():
            student = form.cleaned_data['student']
            exercise = form.cleaned_data['exercise']
            # Check if feedback exists for this student and exercise
            feedback = Feedback.objects.filter(student=student, exercise=exercise).first()
            if feedback:
                # Update existing feedback
                feedback.mistakes = form.cleaned_data['mistakes']
                feedback.suggestions = form.cleaned_data.get('suggestions', feedback.suggestions)
                feedback.score = form.cleaned_data['score']
                feedback.save()
                messages.success(request, 'Feedback updated successfully.')
            else:
                form.save()
                messages.success(request, 'Feedback created successfully.')
            return redirect('ta_dashboard')
    else:
        form = FeedbackForm(subject=subject)
    return render(request, 'feedback/create_feedback.html', {'subject': subject, 'form': form})
    # exercises = Exercise.objects.filter(subject=subject)
    # students = Student.objects.filter(subjects=subject)
    # if request.method == 'POST':
    #     exercise_id = request.POST.get('exercise_id')
    #     mistakes = request.POST.get('mistakes')
    #     suggestions = request.POST.get('suggestions')
    #     score = request.POST.get('score')
    #     if exercise_id and mistakes and suggestions and score:
    #         exercise = get_object_or_404(Exercise, id=exercise_id)
    #         Feedback.objects.create(
    #             student=request.user,
    #             exercise=exercise,
    #             mistakes=mistakes,
    #             suggestions=suggestions,
    #             score=score
    #         )
    #         messages.success(request, 'Feedback created successfully.')
    #         return redirect('exercise_detail', exercise_id=exercise_id)
    # print(students[0].get_full_name)
    # return render(request, 'feedback/create_feedback.html', {'subject': subject, 'exercises': exercises, 'students': students})

@login_required
def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})

# BUG:
@login_required
@require_POST
def save_feedback(request):
    subject_id = request.POST.get('subject_id')
    subject = None
    if subject_id:
        subject = Subject.objects.filter(id=subject_id).first()
    if request.method == 'POST' and subject:
        form = FeedbackForm(request.POST, subject=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback saved successfully.')
            return redirect('exercise_list')
    else:
        form = FeedbackForm(subject=subject)
    return render(request, 'feedback/save_feedback.html', {'form': form, 'subject': subject})

# BUG: 
@login_required
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        feedback.mistakes = request.POST.get('mistakes', feedback.mistakes)
        feedback.suggestions = request.POST.get('suggestions', feedback.suggestions)
        feedback.score = request.POST.get('score', feedback.score)
        feedback.save()
        messages.success(request, 'Feedback updated successfully.')
        return redirect('feedback_detail', feedback_id=feedback_id)
    return render(request, 'feedback/edit_feedback.html', {'feedback': feedback})

@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully.')
        return redirect('exercise_list')
    return render(request, 'feedback/delete_feedback.html', {'feedback': feedback})