from django.db import models
import uuid


class STUDENT_COURSE_STATUS(models.TextChoices):
    pending = "pending"
    accepted = "accepted"


class StudentCourse(models.Model):
    status = models.CharField(
        max_length=255, choices=STUDENT_COURSE_STATUS.choices, default=STUDENT_COURSE_STATUS.pending
    )
    student = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="students_courses"
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="students_courses"
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)


