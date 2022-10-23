from django.contrib import admin

from .models import Follow, User

EMPTY_VALUE = '-none-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'username',
        'role',
        'email'
    )
    list_filter = (
        'username',
        'email',
    )
    ordering = ('pk',)
    empty_value_display = EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'follower',
        'author',
    )
    search_fields = (
        'follower__username',
        'author__username',
    )
    empty_value_display = EMPTY_VALUE
