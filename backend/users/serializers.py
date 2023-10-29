from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Account


class AccountSerializer(UserSerializer):
    username = serializers.RegexField(
        regex=r'[\w.@+z-]+\Z',
        max_length=150,
        required=True,
    )
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )
        model = Account

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'is_subscribed': self.get_is_subscribed(instance),
        }

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context['request'].user
            return (
                user.id is not None
                and user.subscriptions.filter(id=obj.id).exists()
            )
        return True
