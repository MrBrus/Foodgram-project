from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'
    username = models.CharField(
        'Username',
        validators=(RegexValidator,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        'Name',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Surname',
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        'Email',
        validators=(EmailValidator,),
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.TextField(
        'Password',
        max_length=100,
        blank=True,
        default='****'
    )
    role = models.CharField(
        'Role',
        choices=ROLES,
        max_length=50,
        default=USER,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'username',
                    'email',
                ],
                name='unique_user'
            )
        ]
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower',
        help_text="Author's follower"
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Author',
        help_text='Recipe author'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=[
                'author',
                'follower',
            ],
            name='unique_following'
        )]
