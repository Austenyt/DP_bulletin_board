from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class User(AbstractUser):
    """
        Пользовательская модель пользователя, расширяющая AbstractUser.
    """
    username = None
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='Почта')
    role_choices = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=role_choices)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_not_blocked = models.BooleanField(default=True, verbose_name='Неблокирован')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'can_block_user',
                'Can block user',
            ),
            (
                'can_view_user_list',
                'Can view user list',
            ),
        ]

    def assign_block_permission(self, user):
        """
            Назначает разрешение на блокировку пользователю.
        """
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(
            codename="can_block_user",
            content_type=content_type,
            defaults={
                'name': 'Can block user',
                'content_type': content_type,
            }
        )
        user.user_permissions.add(permission)

    def assign_user_list_view_permission(self, user):
        """
           Назначает разрешение на просмотр списка пользователей для пользователя.

        """
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(
            codename="can_view_user_list",
            content_type=content_type,
            defaults={
                'name': 'Can view user list',
                'content_type': content_type,
            }
        )
        user.user_permissions.add(permission)
