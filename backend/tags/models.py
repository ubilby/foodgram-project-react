from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(max_length=255)
    color = ColorField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
