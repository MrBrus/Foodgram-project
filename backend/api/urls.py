from django.urls import include, path
from recipes.views import IngredientViewSet, RecipeViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

from .services import ShoppingListViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

subscriptions = CustomUserViewSet.as_view({'get': 'subscriptions',
                                           'delete': 'subscribe',
                                           'post': 'subscribe', })

urlpatterns = [
    path(
        'users/subscriptions/',
        subscriptions,
        name='subscriptions'),
    path(
        'recipes/download_shopping_cart/',
        ShoppingListViewSet.as_view(),
        name='download_shopping_cart',
    ),
    path(
        'users/<int:id>/subscribe/',
        subscriptions,
        name='subscriptions'
    ),
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
