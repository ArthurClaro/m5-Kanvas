from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "username", "email", "password", "is_superuser")
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message="user with this email already exists.",
                    )
                ]
            },
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> Account:
        is_superuser = validated_data.get("is_superuser", False)
        if is_superuser:
            return Account.objects.create_superuser(**validated_data)
        return Account.objects.create_user(**validated_data)
