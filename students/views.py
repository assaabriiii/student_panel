from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import views as auth_views, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import StudentLoginForm
from feedback.models import Feedback, Exercise

class StudentLoginView(auth_views.LoginView):
    form_class = StudentLoginForm
    template_name = 'students/login.html'
    
    def form_valid(self, form):
        login(self.request, form.user_cache)
        return HttpResponseRedirect(self.get_success_url())

@login_required
def dashboard(request):
    feedback_items = Feedback.objects.filter(student=request.user).order_by('-created_at')
    recent_exercises = Exercise.objects.order_by('-created_at')[:5]
    
    return render(request, 'students/dashboard.html', {
        'feedback_items': feedback_items,
        'recent_exercises': recent_exercises
    })