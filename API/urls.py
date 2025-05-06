from django.urls import path
from .views import UniversityNumberLoginAPIView, DashboardAPIView, TADashboardAPIView

urlpatterns = [
    path('login/', UniversityNumberLoginAPIView.as_view(), name='university_number_login'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard_api'),
    path('ta_dashboard/', TADashboardAPIView.as_view(), name='ta_dashboard_api'),
]