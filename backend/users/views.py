from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import CustomUserSerializer, PasswordSerializer


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
