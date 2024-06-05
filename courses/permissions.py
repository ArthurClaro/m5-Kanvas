from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from django.views import View
from contents.models import Content

from courses.models import Course


class IsAdminOrReadOnlySuperUser(BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        return request.user.is_superuser


class IsSuperUser(BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_superuser and request.user.is_authenticated


class IsAdminCourseOrStudentOwner(BasePermission):
    def has_permission(self, request: Request, view: View):
        #
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        return False







class IsCoursesOwner(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        # if request.user.admin
        if request.user.is_superuser:
            return True
        return request.method and SAFE_METHODS

    def has_object_permission(self, request, view: View, obj: Course) -> bool:
        return request.user.is_superuser or request.user in obj.students.all()
    

# class IsCoursesOwner(BasePermission):
#     def has_permission(self, request: Request, view: APIView):
#         # if request.user.is_authenticated and request.method in SAFE_METHODS:
#         #     return True
        
#         if request.user.is_superuser:
#             return True
#         # return request.method and SAFE_METHODS
#         return False

#     def has_object_permission(self, request, view: View, obj: Course) -> bool:
#         # return request.user.is_superuser or request.user in obj.students.all()
#         # if request.user.is_authenticated and request.user in obj.students.all():
#         if request.user.is_authenticated and request.method in SAFE_METHODS:
#             return request.user in obj.students.all()
#         return False

        # return request.user.is_authenticated and obj == request.user







class ContentAndOwner(BasePermission):
    def has_permission(self, request: Request, view: View):
        #
        if request.user.is_superuser:
            return True
        
        return request.method and SAFE_METHODS
    
    def has_object_permission(self, request, view: View, obj: Content) -> bool:
        return request.user.is_superuser or request.user in obj.course.students.all()
