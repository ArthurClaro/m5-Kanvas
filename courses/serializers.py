from rest_framework import serializers
from accounts.models import Account

from contents.serializers import ContentSerializer
from students_courses.serializers import StudentCourseSerializer

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        ]
        extra_kwargs = {
            "contents": {
                "read_only": True,
            },
            "students_courses": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        return Course.objects.create(**validated_data)


class StudentNNSerializer(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "students_courses",
        ]
        depth = 1
        # read_only_fields = ["name"]
        extra_kwargs = {
            "name": {
                "read_only": True,
            },
        }

    def update(self, instance, validated_data):
        studentData = validated_data["students_courses"]
        studentUpdate = []
        studentNone = []

        # for student in studentData:
        #     email = student["student"]["email"]
        #     student = Account.objects.filter(email=email).first()
        #     if not student:
        #         studentNone.append(email)
        #     else:
        #         studentUpdate.append(student)
        for student in studentData:
            student2 = student["student"]
            email = Account.objects.filter(email=student2["email"]).first()
            if email is None:
                studentNone.append(student2["email"])
            else:
                studentUpdate.append(email)

        if studentNone:
            message = ", ".join(studentNone)
            raise serializers.ValidationError(
                {"detail": f"No active accounts was found: {message}."}
            )
        if not self.partial:
            instance.students.add(*studentUpdate)
            return instance

        # instance.students.add(*studentUpdate)

        return super().update(instance, validated_data)
