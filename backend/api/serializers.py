from rest_framework import serializers
from djoser.serializers import UserSerializer


from recipes.models import CustomUser, Recipe, Tag
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
            'auth_token',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'password'
        )
        model = CustomUser

    def create(self, validated_data):
        password = validated_data.pop('password')
        re_password = validated_data.pop('re_password', None)
        if re_password and password != re_password:
            raise serializers.ValidationError('Пароли не совпадают.')
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


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
