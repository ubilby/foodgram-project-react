from django.db import models
from django.core.validators import RegexValidator


class Tag(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, validators=[RegexValidator(
        r'^#[0-9A-Fa-f]{6}$', message="Неверный формат цвета.")])
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
