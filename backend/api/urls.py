from django.urls import include, path

from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagsViewSet
from users.views import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

subscriptions = CustomUserViewSet.as_view({'get': 'subscriptions',
                                           'delete': 'subscribe',
                                           'post': 'subscribe', })
download = RecipeViewSet.as_view({'get': 'download_shopping_cart'})

urlpatterns = [
    path(
        'users/subscriptions/',
        subscriptions,
        name='subscriptions'),
    path(
        'recipes/download_shopping_cart/',
        download,
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
