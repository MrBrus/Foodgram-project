from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (
    CustomUserSerializer, PasswordSerializer, SubscriptionsSerializer
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        context = {'request': self.request}
        serializer = CustomUserSerializer(
            request.user,
            context=context
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request, pk=None):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = PasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        followed = get_object_or_404(User, id=id)
        follower = request.user

        if request.method == 'POST':
            subscribed = (
                Follow.objects.filter(
                    author=followed,
                    follower=follower
                ).exists()
            )
            if subscribed is True:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.get_or_create(
                follower=follower,
                author=followed
            )
            serializer = SubscriptionsSerializer(
                context=self.get_serializer_context()
            )
            return Response(serializer.to_representation(
                instance=followed),
                status=status.HTTP_201_CREATED
            )
        Follow.objects.filter(
            follower=follower, author=followed
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions',
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(followed__follower=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
