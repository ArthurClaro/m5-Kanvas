from contents.models import Content
from contents.serializers import ContentSerializer
from courses.permissions import (
    ContentAndOwner,
    IsAdminCourseOrStudentOwner,
    IsAdminOrReadOnlySuperUser,
    IsCoursesOwner,
    IsSuperUser,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from courses.serializers import CourseSerializer, StudentNNSerializer
from students_courses.models import StudentCourse
from students_courses.serializers import StudentCourseSerializer
from .models import Course
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound


class CourseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminCourseOrStudentOwner]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CourseSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(students=user)

        return queryset


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCoursesOwner]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# /////////////// Content


class ContentsCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def perform_create(self, serializer):
        course = Course.objects.filter(pk=self.kwargs["pk"]).first()
        if not course:
            raise NotFound({"detail": "courses not found."})
        serializer.save(course=course)


# /api/courses/<course_id>/contents/<content_id>/
# get/patch/del


class ContentsDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ContentAndOwner]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "content_id"

    def get_object(self):
        try:
            course_id = self.kwargs["course_id"]
            content_id = self.kwargs["content_id"]
            Course.objects.get(id=course_id)
            content = Content.objects.get(id=content_id)
        except Course.DoesNotExist:
            raise NotFound({"detail": "course not found."})
        except Content.DoesNotExist:
            raise NotFound({"detail": "content not found."})
        self.check_object_permissions(self.request, content)
        return content


# /////////////// Student

# /api/courses/<course_id>/students/
# get / put


class StudentView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    queryset = Course.objects.all()
    serializer_class = StudentNNSerializer
    lookup_url_kwarg = "course_id"
