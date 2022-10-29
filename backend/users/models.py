from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'
    username = models.CharField(
        'Username',
        validators=(RegexValidator,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text='Enter your username'
    )
    first_name = models.CharField(
        'Name',
        max_length=150,
        blank=True,
        help_text='Enter your name. It will show up under your recipes.'
    )
    last_name = models.CharField(
        'Surname',
        max_length=150,
        blank=True,
        help_text='Enter your lastname. It will show up under your recipes.'
    )
    email = models.EmailField(
        'Email',
        validators=(EmailValidator,),
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        help_text='Enter your email address.'
    )
    password = models.TextField(
        'Password',
        max_length=100,
        blank=True,
        help_text='Your password must be larger than 8 symbols.'
    )
    role = models.CharField(
        'Role',
        choices=ROLES,
        max_length=50,
        default=USER,
        blank=True,
        help_text="Change the user's role."
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_user(self):
        return self.role == User.USER


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

    def __str__(self):
        return f'{self.follower} subscribed on {self.author}'
