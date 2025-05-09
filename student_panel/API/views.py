from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentLoginSerializer, CourseSerializer, ExerciseSerializer, FeedbackSerializer, CommentSerializer, AnnouncementSerializer
from .models import Student, Course, Exercise, Comment, Announcement, TAAssignment, Professor
from datetime import date


class StudentLoginView(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    student = Student.objects.get(user=user)
                except Student.DoesNotExist:
                    return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# not tested
class StudentCourseView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            course = student.enrolled_courses.get(course_id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found or not enrolled.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response({'course': serializer.data})


class StudentCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        courses = student.enrolled_courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response({'courses': serializer.data})
    

# not tested
class StudentExerciseView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        exercise_id = request.query_params.get('exercise_id')
        if not exercise_id:
            return Response({'error': 'exercise_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            exercise = Exercise.objects.get(exercise_id=exercise_id, course__in=student.enrolled_courses.all())
        except Exercise.DoesNotExist:
            return Response({'error': 'Exercise not found or not accessible.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExerciseSerializer(exercise)
        return Response({'exercise': serializer.data})


class StudentExercisesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        curr_courses = student.enrolled_courses.filter()
        exercises = Exercise.objects.filter(course__in=curr_courses)
        serializer = ExerciseSerializer(exercises, many=True)
        return Response({'exercises': serializer.data})
    

class StudentCurrExerciseView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        today = date.today()
        curr_courses = student.enrolled_courses.filter(
            end_date__gte=today
        )
        exercises = Exercise.objects.filter(course__in=curr_courses)
        serializer = ExerciseSerializer(exercises, many=True)
        return Response({'exercises': serializer.data})
    
    
# not tested
class StudentCourseExercisesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            course = student.enrolled_courses.get(course_id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found or not enrolled.'}, status=status.HTTP_404_NOT_FOUND)
        exercises = Exercise.objects.filter(course=course)
        serializer = ExerciseSerializer(exercises, many=True)
        return Response({'exercises': serializer.data})


# not tested
class StudentExerciseFeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        exercise_id = request.query_params.get('exercise_id')
        if not exercise_id:
            return Response({'error': 'exercise_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            exercise = Exercise.objects.get(exercise_id=exercise_id, course__in=student.enrolled_courses.all())
        except Exercise.DoesNotExist:
            return Response({'error': 'Exercise not found or not accessible.'}, status=status.HTTP_404_NOT_FOUND)
        feedback = getattr(exercise, 'feedback', None)
        serializer = FeedbackSerializer({'feedback': feedback})
        return Response(serializer.data)


# not tested
class StudentLastFiveExercisesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        courses = student.enrolled_courses.all()
        exercises = Exercise.objects.filter(course__in=courses).order_by('-date')[:5]
        serializer = ExerciseSerializer(exercises, many=True)
        return Response({'exercises': serializer.data})
    

class ExerciseCommentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        exercise_id = request.query_params.get('exercise_id')
        if not exercise_id:
            return Response({'error': 'exercise_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            exercise = Exercise.objects.get(exercise_id=exercise_id, course__in=student.enrolled_courses.all())
        except Exercise.DoesNotExist:
            return Response({'error': 'Exercise not found or not accessible.'}, status=status.HTTP_404_NOT_FOUND)
        comments = exercise.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response({'comments': serializer.data})

# not tested
class StudentAnnouncementsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'error': 'No student profile found for this user.'}, status=status.HTTP_403_FORBIDDEN)
        courses = student.enrolled_courses.all()
        announcements = Announcement.objects.filter(course__in=courses).order_by('-created_at')
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response({'announcements': serializer.data})


# not tested
# BUG: Only can be made from TA and professor of that specific course
class CreateAnnouncementView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        title = request.data.get('title')
        body = request.data.get('body')
        if not course_id or not title or not body:
            return Response({'error': 'course_id, title, and body are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Check if user is TA or Professor for the course
        is_ta = TAAssignment.objects.filter(student__user=user, course=course).exists()
        is_prof = Professor.objects.filter(user=user, courses=course).exists()
        if not (is_ta or is_prof):
            return Response({'error': 'Only TAs or Professors of this course can create announcements.'}, status=status.HTTP_403_FORBIDDEN)
        announcement = Announcement.objects.create(
            author=user,
            course=course,
            title=title,
            body=body
        )
        serializer = AnnouncementSerializer(announcement)
        return Response({'announcement': serializer.data}, status=status.HTTP_201_CREATED)