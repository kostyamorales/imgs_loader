from django.db import models


class Image(models.Model):
    img = models.ImageField('Картинка')
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
