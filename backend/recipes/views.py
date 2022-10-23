from io import BytesIO

from django.db.models import Sum
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .permissions import OwnerOrReadOnly
from .serializers import (SerializerFavorite, SerializerIngredient,
                          SerializerRecipe, SerializerRecipeView,
                          SerializerTag)


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
    serializer = SerializerFavorite(
        recipe,
        context={
            "request": request
        }
    )
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


class ViewSetTags(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = SerializerTag
    permission_classes = (AllowAny,)
    pagination_class = None
    http_method_names = ['get']


class ViewSetIngredient(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = SerializerIngredient
    permission_classes = (AllowAny,)
    filter = IngredientFilter
    search_fields = ('^name',)
    pagination_class = None
    http_method_names = ['get']


class ViewSetRecipe(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = SerializerRecipeView
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (OwnerOrReadOnly,)
    filterset_class = RecipeFilter
    ordering_fields = ('-pub_date',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return SerializerRecipe
        elif self.request.method == 'GET':
            return SerializerRecipeView

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteView(APIView):
    def delete(self, request, id):
        return delete(request, id, Favorite)

    def post(self, request, id):
        return post(request, id, Favorite)


class ViewSetShoppingCart(APIView):
    def delete(self, request, id):
        return delete(request, id, ShoppingCart)

    def post(self, request, id):
        return post(request, id, ShoppingCart)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def get(self, request):
        font = 'arial'
        pdfmetrics.registerFont(
            TTFont(
                'arial',
                'arial.ttf',
                'UTF-8'
            )
        )
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.setFont(font, 24)
        pdf.drawString(150, 800, 'Shopping list')
        pdf.setFont(font, 14)
        from_bottom = 700
        ingredients = IngredientInRecipe.objects.filter(
            recipes__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        for ingredient in ingredients:
            shopping_cart = '\n'.join([
                f"{ingredient['ingredient__name']} - {ingredient['amount']} ''"
                f"{ingredient['ingredient__measurement_unit']}"
            ])
            pdf.drawString(50, from_bottom, shopping_cart)
            from_bottom -= 20
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            content_type='application/pdf',
            as_attachment=True,
        )
