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
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeViewSerializer,
                          TagSerializer)


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
    permission_classes = (OwnerOrReadOnly,)
    filterset_class = RecipeFilter
    ordering_fields = ('-pub_date',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeSerializer
        elif self.request.method == 'GET':
            return RecipeViewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(APIView):
    def delete(self, request, id):
        return delete(request, id, Favorite)

    def post(self, request, id):
        return post(request, id, Favorite)


class ShoppingCartViewSet(APIView):
    def delete(self, request, id):
        return delete(request, id, ShoppingCart)

    def post(self, request, id):
        return post(request, id, ShoppingCart)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def create_pdf(self, request):
        font = 'arial'
        pdfmetrics.registerFont(
            TTFont(
                'arial',
                'arial.ttf',
                'UTF-8'
            )
        )
        font_size_title = 24
        font_size_text = 14
        pixels_from_top_title = 150
        pixels_from_down_title = 800
        pixels_from_left_text = 50
        pixels_from_bottom_text_str = 700
        pixels_subtraction = 20

        buffer = BytesIO()
        buffer_seek_count = 0
        pdf = canvas.Canvas(buffer)
        pdf.setFont(font, font_size_title)
        pdf.drawString(
            pixels_from_top_title,
            pixels_from_down_title,
            'Shopping list'
        )
        pdf.setFont(font, font_size_text)

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
            pdf.drawString(
                pixels_from_left_text,
                pixels_from_bottom_text_str,
                shopping_cart
            )
            pixels_from_bottom_text_str -= pixels_subtraction
        pdf.showPage()
        pdf.save()
        buffer.seek(buffer_seek_count)
        return FileResponse(
            buffer,
            content_type='application/pdf',
            as_attachment=True,
        )
