from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializer import UniversityNumberLoginSerializer
from rest_framework.permissions import IsAuthenticated
from .serializer import SubjectSerializer, FeedbackSerializer, ExerciseSerializer
from feedback.models import Feedback, Exercise, Presence
from rest_framework.authtoken.models import Token

User = get_user_model()

class UniversityNumberLoginAPIView(APIView):
    def post(self, request):
        serializer = UniversityNumberLoginSerializer(data=request.data)
        if serializer.is_valid():
            university_number = serializer.validated_data['university_number']
            user = User.objects.filter(university_number=university_number).first()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'id': user.id,
                    'username': user.username,
                    'university_number': user.university_number,
                    'email': user.email,
                    'token': token.key,
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid university number'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        subjects = user.subjects.all() if hasattr(user, 'subjects') else []
        feedback_items = Feedback.objects.filter(student=user, exercise__subject__in=subjects).order_by('-created_at')
        recent_exercises = Exercise.objects.filter(subject__in=subjects).order_by('-created_at')[:5]
        return Response({
            'subjects': SubjectSerializer(subjects, many=True).data,
            'feedback_items': FeedbackSerializer(feedback_items, many=True).data,
            'recent_exercises': ExerciseSerializer(recent_exercises, many=True).data
        })


class TADashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'is_ta') or not user.is_ta:
            return Response({'detail': 'You are not authorized to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        ta_subjects = user.ta_subjects.all() if hasattr(user, 'ta_subjects') else []
        exercises = Exercise.objects.filter(subject__in=ta_subjects).order_by('-created_at')
        return Response({
            'ta_subjects': SubjectSerializer(ta_subjects, many=True).data,
            'exercises': ExerciseSerializer(exercises, many=True).data
        })


class MarkAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from .serializer import MarkAttendanceSerializer
        serializer = MarkAttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        subject_id = serializer.validated_data['subject_id']
        attendance = serializer.validated_data['attendance']
        # Only TAs, and only for subjects they’re assigned to
        if not getattr(user, 'is_ta', False) or not user.ta_subjects.filter(id=subject_id).exists():
            return Response({'detail': 'You are not authorized to mark attendance for this subject.'}, status=status.HTTP_403_FORBIDDEN)
        from students.models import Subject, Student
        from datetime import date
        subject = Subject.objects.filter(id=subject_id).first()
        if not subject:
            return Response({'detail': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)
        today = date.today()
        for entry in attendance:
            student_id = entry['student_id']
            present = entry['present']
            student = Student.objects.filter(id=student_id).first()
            if not student or not subject.students.filter(id=student_id).exists():
                continue
            Presence.objects.update_or_create(
                subject=subject,
                student=student,
                date=today,
                defaults={
                    'present': present,
                    'marked_by': user,
                }
            )
        return Response({'detail': f'Attendance for {subject.name} on {today:%Y-%m-%d} saved.'}, status=status.HTTP_200_OK)

