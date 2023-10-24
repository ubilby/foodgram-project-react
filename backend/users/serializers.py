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

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'There is user with this username'
            )
        return username_validator(value)
