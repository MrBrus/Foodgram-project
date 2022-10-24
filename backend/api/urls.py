from api.views import ListSubscriptionsViewSet, SubscribeViewSet
from django.urls import include, path
from recipes.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                           ShoppingCartViewSet, TagsViewSet)
from rest_framework.routers import DefaultRouter, SimpleRouter
from users.views import CustomUserViewSet

app_name = 'api'
router = SimpleRouter()
router_2 = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router_2.register(r'', ListSubscriptionsViewSet, basename='subscriptions')

urlpatterns = [

    path(
        'recipes/<int:id>/favorite/',
        FavoriteViewSet.as_view(),
        name='favorite',
    ),
    path(
        'recipes/download_shopping_cart/',
        ShoppingCartViewSet.as_view(),
        name='download_shopping_cart',
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShoppingCartViewSet.as_view(),
        name='shopping_cart',
    ),
    path(
        'users/subscriptions/',
        include(router_2.urls)
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscribeViewSet.as_view(),
        name="subscribe"),
    path(
        'auth/',
        include('djoser.urls.authtoken')
    ),
    path(
        '',
        include(router.urls)
    ),
    path(
        '',
        include('djoser.urls')
    ),

]
