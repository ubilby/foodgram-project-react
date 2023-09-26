from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipes.models import CustomUser
from recipes.validators import username_validator


class UserSerializer(ModelSerializer):
    username = serializers.RegexField(
        regex=r'[\w.@+-]+\Z',
        max_length=150,
        required=True,
    )

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = CustomUser

    def validate_role(self, value):
        roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
        if value not in roles:
            raise serializers.ValidationError('Несуществующая роль.')
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        return username_validator(value)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
    )

    class Meta:
        fields = ('email', 'username')
        model = CustomUser

    def validate_username(self, value):
        return username_validator(value)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
