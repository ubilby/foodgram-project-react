from django.db import models
from users.models import Account


class Subscribe(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber',
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='subscribing',
        blank=False,
        null=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscribing'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_cannot_follow_themselves'
            )
        ]
