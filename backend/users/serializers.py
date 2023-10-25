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
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
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
            'last_name': instance.last_name,
            'is_subscribed': self.get_is_subscribed(instance),
        }

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'There is user with this username'
            )
        return username_validator(value)

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context['request'].user
            return (
                user.id is not None
                and user.subscriber.filter(author=obj).exists()
            )
        return True
