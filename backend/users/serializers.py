from rest_framework import serializers
from djoser.serializers import UserSerializer

from users.models import Account
from backend.validators import username_validator


class AccountSerializer(UserSerializer):
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
            'password'
        )
        model = Account

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Account(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name
        }

    def validate_role(self, value):
        roles = [choice[0] for choice in Account.ROLE_CHOICES]
        if value not in roles:
            raise serializers.ValidationError('Несуществующая роль.')
        return value

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        return username_validator(value)


class AccountGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context['request'].user
            return (
                user.id is not None
                and len(user.subscriber.filter(author=obj)) > 0
            )
        return True


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
