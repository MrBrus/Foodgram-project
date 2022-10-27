from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe

from .models import Follow, User


class UserRegistrationSerializer(UserCreateSerializer):
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


class CustomUserSerializer(UserSerializer):
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
        return Follow.objects.filter(
            follower=user,
            author=author
        ).exists()


class PasswordSerializer(serializers.ModelSerializer):
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


class FollowingRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionsSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def validate(self, data):
        author = data['followed']
        follower = data['follower']
        if follower == author:
            raise serializers.ValidationError('You can`t follow for yourself!')
        if Follow.objects.filter(author=author, follower=follower).exists():
            raise serializers.ValidationError('You have already subscribed!')
        return data

    def get_recipes(self, author):
        limit_recipes_show = 3
        recipes = author.recipes.all()[:limit_recipes_show]
        return FollowingRecipeSerializer(
            recipes,
            many=True
        ).data

    def get_is_subscribed(self, author):
        user = self.context['request'].user.id
        return Follow.objects.filter(
            follower=user,
            author=author
        ).exists()

    def get_recipes_count(self, author):
        return author.recipes.count()
