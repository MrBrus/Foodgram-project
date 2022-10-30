from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from recipes.services import get_pdf
from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import OwnerOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeViewSerializer,
    TagSerializer
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
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
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
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return RecipeSerializer
        return RecipeViewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def delete_fav_or_shoplist(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
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

    def post_fav_or_shoplist(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        serializer = FavoriteSerializer(
            recipe,
            context=self.get_serializer_context()
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True,
            methods=['post'])
    def favorite(self, request, pk):
        user = request.user
        return self.post_fav_or_shoplist(Favorite, user, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        return self.delete_fav_or_shoplist(Favorite, user, pk)

    @action(detail=True,
            methods=['post'])
    def shopping_cart(self, request, pk):
        user = request.user
        return self.post_fav_or_shoplist(ShoppingCart, user, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        return self.delete_fav_or_shoplist(ShoppingCart, user, pk)

    @action(
        detail=False,
        methods=['GET'],
    )
    def download_shopping_cart(self, request):
        user = request.user
        return get_pdf(user)
