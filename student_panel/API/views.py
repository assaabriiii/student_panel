from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentLoginSerializer, CourseSerializer, ExerciseSerializer
from .models import Student, Course, Exercise
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


class StudentExerciseView(APIView):
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