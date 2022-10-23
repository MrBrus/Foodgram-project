from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Follow, User

from .pagination import LimitPagination
from .serializers import SubscriptionsSerializer


class ListSubscriptions(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer
    pagination_class = LimitPagination

    def get_queryset(self):
        return User.objects.filter(followed__follower=self.request.user)


class Subscribe(APIView):
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
