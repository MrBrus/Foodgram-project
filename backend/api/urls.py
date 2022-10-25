from api.views import ListSubscriptionsViewSet, SubscribeViewSet
from django.urls import include, path
from recipes.views import (IngredientViewSet, RecipeViewSet,TagsViewSet,
                           ShoppingCartViewSet)
from rest_framework.routers import DefaultRouter, SimpleRouter
from users.views import CustomUserViewSet
from .services import ShoppingListViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
app_name = 'api'
router = SimpleRouter()
router_2 = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router_2.register('', ListSubscriptionsViewSet, basename='subscriptions')


urlpatterns = [

    path(
        'recipes/<int:id>/favorite/',
        RecipeViewSet.as_view(({'POST': 'favorite',
                                'DELETE': 'favorite'})),
        name='favorite',
    ),
    path(
        'recipes/download_shopping_cart/',
        ShoppingListViewSet.as_view(),
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
