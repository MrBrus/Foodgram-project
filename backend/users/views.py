from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import LimitPagination
from .models import User, Follow
from .serializers import (CustomUserSerializer, PasswordSerializer,
                          SubscriptionsSerializer, FollowingRecipeSerializer)


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

    @action(detail=False,
            methods=['post'],
            permission_classes=(IsAuthenticated,))
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


class ListSubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer
    pagination_class = LimitPagination

    def get_queryset(self):
        return User.objects.filter(followed__follower=self.request.user)


class SubscribeViewSet(APIView):
    def delete(self, request, id=None):
        follower = request.user
        author = get_object_or_404(
            User,
            id=id,
        )
        if follower == author:
            return Response(
                {'errors': 'You cant unsubscribe from yourself.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow = Follow.objects.filter(
            follower=follower,
            author=author,
        )
        if follow.exists():
            follow.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {'errors': 'You are finally unsubscribed.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, id=None):
        follower = request.user
        author = get_object_or_404(User, id=id)
        if follower == author:
            return Response(
                {'errors': 'You cant subscribe yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
                follower=follower,
                author=author,
        ).exists():
            return Response(
                {'errors': 'You are finally subscribed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.get_or_create(
            follower=follower,
            author=author
        )
        serializer = SubscriptionsSerializer(
            author,
            context={
                'request': request
            },
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
