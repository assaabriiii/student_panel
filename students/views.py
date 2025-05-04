from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import StudentLoginForm, ExerciseForm
from feedback.models import Feedback, Exercise, Presence
from django.contrib.auth import logout
from .models import Subject
from datetime import date
from django.contrib import messages


class StudentLoginView(auth_views.LoginView):
    form_class = StudentLoginForm
    template_name = 'students/login.html'
    
    def form_valid(self, form):
        login(self.request, form.user_cache)
        role = self.request.POST.get('role')
        user = form.user_cache
        if role == 'ta' and hasattr(user, 'is_ta') and user.is_ta:
            print("/////////////////////////////////////////////////////CHECKED")
            return HttpResponseRedirect(reverse('ta_dashboard'))
        return HttpResponseRedirect(self.get_success_url())

@login_required
def dashboard(request):
    user = request.user
    # Only show subjects the student is enrolled in
    subjects = user.subjects.all() if hasattr(user, 'subjects') else []
    # Only show feedback for exercises in those subjects
    feedback_items = Feedback.objects.filter(student=user, exercise__subject__in=subjects).order_by('-created_at')
    # Only show exercises for those subjects
    recent_exercises = Exercise.objects.filter(subject__in=subjects).order_by('-created_at')[:5]
    
    return render(request, 'students/dashboard.html', {
        'feedback_items': feedback_items,
        'recent_exercises': recent_exercises,
        'subjects': subjects
    })


def Logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required
def ta_dashboard(request):
    user = request.user
    ta_subjects = user.ta_subjects.all() if hasattr(user, 'ta_subjects') else []
    # Fetch all exercises for TA's subjects
    exercises = Exercise.objects.filter(subject__in=ta_subjects).order_by('-created_at')
    return render(request, 'students/ta_dashboard.html', {'ta_subjects': ta_subjects, 'exercises': exercises})


@login_required
def mark_attendance(request, subject_id):
    user = request.user
    # 1) Only TAs, and only for subjects they’re assigned to
    if not getattr(user, 'is_ta', False) or not user.ta_subjects.filter(id=subject_id).exists():
        return HttpResponseForbidden("You are not authorized to mark attendance for this subject.")

    subject = get_object_or_404(Subject, id=subject_id)
    students = list(subject.students.all())
    today = date.today()

    # Fetch last N sessions (dates) for this subject
    N = 5
    session_dates = list(Presence.objects.filter(subject=subject)
                        .order_by('-date')
                        .values_list('date', flat=True)
                        .distinct())
    if today not in session_dates:
        session_dates = [today] + session_dates
    session_dates = session_dates[:N]
    session_dates = sorted(session_dates)

    # Build attendance matrix: {student_id: {date: present}}
    attendance_matrix = {student.id: {} for student in students}
    presences = Presence.objects.filter(subject=subject, date__in=session_dates)
    for presence in presences:
        attendance_matrix[presence.student_id][presence.date] = presence.present

    if request.method == 'POST':
        for student in students:
            present = request.POST.get(f'student_{student.id}') == 'on'
            Presence.objects.update_or_create(
                subject=subject,
                student=student,
                date=today,
                defaults={
                    'present': present,
                    'marked_by': user,
                }
            )
        messages.success(request, f"Attendance for {subject.name} on {today:%Y-%m-%d} saved.")
        return HttpResponseRedirect(reverse('ta_dashboard'))

    # For current session, pre-check boxes
    existing = Presence.objects.filter(subject=subject, date=today)
    present_ids = set(existing.filter(present=True).values_list('student_id', flat=True))

    return render(request, 'attendance/mark_attendance.html', {
        'subject': subject,
        'students': students,
        'present_ids': present_ids,
        'today': today,
        'session_dates': session_dates,
        'attendance_matrix': attendance_matrix,
    })
    

@login_required
def add_exercise(request):
    user = request.user
    ta_subjects = user.ta_subjects.all() if hasattr(user, 'ta_subjects') else []
    if request.method == 'POST':
        form = ExerciseForm(request.POST, ta_subjects=ta_subjects)
        if form.is_valid():
            exercise = form.save()
            messages.success(request, f"Exercise «{exercise.title}» created.")
            return redirect('ta_dashboard')
    else:
        form = ExerciseForm(ta_subjects=ta_subjects)
    return render(request, 'exercises/add_exercise.html', {'form': form})

@login_required
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    # optionally check permissions: only creator or professor
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, f"Exercise «{exercise.title}» deleted.")
        return redirect('ta_dashboard')
    return render(request, 'exercises/confirm_delete_exercise.html', {
        'exercise': exercise
    })