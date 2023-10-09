from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserSerializer

from .models import Subscribe
from recipes.models import CustomUser
from .validators import username_validator


class CustomUserSerializer(UserSerializer):
    username = serializers.RegexField(
        regex=r'[\w.@+z-]+\Z',
        max_length=150,
        required=True,
    )

    class Meta:
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        model = CustomUser

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
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


class CustomUserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            not user.id == None and
            len(user.subscriber.filter(author=obj)) > 0
        )


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('author',)

    def validate_author(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на себя.")
        return value
