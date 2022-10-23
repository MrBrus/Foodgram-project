from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow, User


class SerializerUserRegistration(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'username',
            'email',
            'id',
            'password',
            'first_name',
            'last_name',
            'role',
        ]
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=[
                'username',
                'email',
            ],
            message='Username or email are used.',
        )]


class SerializerCustomUser(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'id',
            'first_name',
            'last_name',
            'is_subscribed',
            'role',
        ]

    def get_is_subscribed(self, author):
        user = self.context['request'].user.id
        if Follow.objects.filter(
                author=author,
                follower=user
        ).exists():
            return True
        return False


class SerializerPassword(serializers.ModelSerializer):
    current_password = serializers.CharField(
        required=True,
    )
    new_password = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'current_password',
            'new_password'
        )
