from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import OwnerOrReadOnly
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeSerializer,
    RecipeViewSerializer, TagSerializer
)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    http_method_names = ['get']


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter = IngredientFilter
    search_fields = ('^name',)
    pagination_class = None
    http_method_names = ['get']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeViewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (OwnerOrReadOnly,)
    filterset_class = RecipeFilter
    ordering_fields = ('-pub_date',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return RecipeSerializer
        elif self.request.method == 'GET':
            return RecipeViewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def delete(request, id, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if not model.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            return Response(
                {
                    'errors': 'Delete is not available.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = get_object_or_404(
            model,
            user=user,
            recipe=recipe
        )
        obj.delete()
        return Response(
            {'errors': 'Successfully delete.'},
            status=status.HTTP_204_NO_CONTENT,
        )

    def post(request, id, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if model.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            return Response(
                {
                    'errors': 'Available right now.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        serializer = FavoriteSerializer(
            recipe,
            context={
                "request": request
            }
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True,
            methods=['post'])
    def favorite(self, request, pk):
        return RecipeViewSet.post(request, pk, Favorite)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return RecipeViewSet.delete(request, pk, Favorite)

    @action(detail=True,
            methods=['post'])
    def shopping_cart(self, request, pk):
        return RecipeViewSet.post(request, pk, ShoppingCart)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return RecipeViewSet.delete(request, pk, ShoppingCart)

# class FavoriteViewSet(APIView):
#     def delete(self, request, id):
#         return RecipeViewSet.delete(request, id, Favorite)
#
#     def post(self, request, id):
#         return RecipeViewSet.post(request, id, Favorite)


# class ShoppingCartViewSet(APIView):
#     def delete(self, request, id):
#         return RecipeViewSet.delete(request, id, ShoppingCart)
#
#     def post(self, request, id):
#         return RecipeViewSet.post(request, id, ShoppingCart)
