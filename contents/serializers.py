from rest_framework import serializers


from .models import Content


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = [
            "id",
            "name",
            "content",
            "video_url",
        ]

    def create(self, validated_data):
        return Content.objects.create(**validated_data)
