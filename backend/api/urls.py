from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.views import ListSubscriptions, Subscribe
from recipes.views import (FavoriteView, ViewSetIngredient, ViewSetRecipe,
                           ViewSetShoppingCart, ViewSetTags)
from users.views import ViewSetCustomUser

app_name = 'api'
router = SimpleRouter()
router_2 = DefaultRouter()
router.register(r'users', ViewSetCustomUser, basename='users')
router.register(r'tags', ViewSetTags, basename='tags')
router.register(r'ingredients', ViewSetIngredient, basename='ingredients')
router.register(r'recipes', ViewSetRecipe, basename='recipes')
router_2.register(r'', ListSubscriptions, basename='subscriptions')

urlpatterns = [

    path(
        'recipes/<int:id>/favorite/',
        FavoriteView.as_view(),
        name='favorite',
    ),
    path(
        'recipes/download_shopping_cart/',
        ViewSetShoppingCart.as_view(),
        name='download_shopping_cart',
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ViewSetShoppingCart.as_view(),
        name='shopping_cart',
    ),
    path(
        'users/subscriptions/',
        include(router_2.urls)
    ),
    path(
        'users/<int:id>/subscribe/',
        Subscribe.as_view(),
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
