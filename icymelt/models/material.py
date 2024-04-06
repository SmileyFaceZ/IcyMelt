"""This module contains the Material model."""
from django.db import models


class Material(models.Model):
    """A model to represent material type."""
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.type