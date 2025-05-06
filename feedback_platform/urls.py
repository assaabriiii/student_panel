from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard/', permanent=True)),
    path('', include('students.urls')),
    path('feedback/', include('feedback.urls')),
    path('api/', include('API.urls')),
]