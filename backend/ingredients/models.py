from django.db import models


class Ingredients(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=2)

    def __str__(self):
        return self.name
