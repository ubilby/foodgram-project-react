from django.db import models

from users.models import CustomUser


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber',
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='subscribing',
        blank=False,
        null=False,
    )

    class Meta:
        models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_following'
        )
