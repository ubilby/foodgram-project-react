from rest_framework import serializers
from djoser.serializers import UserSerializer


from recipes.models import CustomUser
from recipes.validators import username_validator


class CustomUserSerializer(UserSerializer):
    username = serializers.RegexField(
        regex=r'[\w.@+z-]+\Z',
        max_length=150,
        required=True,
    )

    auth_token = serializers.CharField(
        required=False, read_only=True
    )

    class Meta:
        fields = (
            "auth_token",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password"
        )
        model = CustomUser

    def create(self, validated_data):
        # Извлекаем пароль из данных
        password = validated_data.pop('password')

        # Создаем пользователя
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

    #     # Создаем и связываем токен
    #     token, _ = Token.objects.get_or_create(user=user)
    #     user.auth_token = token
        user.save()

        return user

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
