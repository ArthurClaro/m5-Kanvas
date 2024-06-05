from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.CourseView.as_view()),
    path("courses/<str:pk>/", views.CourseDetailView.as_view()),
    path("courses/<str:pk>/contents/", views.ContentsCreateView.as_view()),
    path("courses/<str:course_id>/contents/<str:content_id>/", views.ContentsDetailView.as_view()),
    path("courses/<str:course_id>/students/", views.StudentView.as_view()),
    
]
