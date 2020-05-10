from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Material(models.Model):
    name = models.CharField(max_length=64, db_index=True, verbose_name=_('name'))
    characteristics = models.TextField(blank=True, db_index=True)

    def __str__(self):
        return self.name


class Tool(models.Model):
    PENCIL = 1
    PEN = 2
    BRUSH = 3
    PAINT = 4
    PASTEL = 5
    CHARCOAL = 6

    TYPE_CHOICES = (
        (PENCIL, 'pencil'),
        (PEN, 'pen'),
        (BRUSH, 'brush'),
        (PAINT, 'paint'),
        (PASTEL, 'pastel'),
        (CHARCOAL, 'charcoal'),
    )

    name = models.CharField(max_length=64, db_index=True, verbose_name=_('name'))
    tool_type = models.IntegerField(choices=TYPE_CHOICES, db_index=True, verbose_name=_('tool type'))
    materials = models.ManyToManyField(Material, db_index=True, verbose_name=_('materials'), blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name=_('name'))
    artist = models.CharField(max_length=64, blank=True, db_index=True, verbose_name=_('artist'))
    file = models.ImageField(db_index=True, verbose_name=_('file'))
    colours = ArrayField(models.CharField(max_length=7), blank=True, db_index=True, verbose_name=_('colours'))
    description = models.TextField(blank=True, db_index=True, verbose_name=_('description'))
    tools = models.ManyToManyField(Tool, db_index=True, verbose_name=_('tools'), blank=True)

    def get_absolute_url(self):
        return reverse('core:image_detail', args=[self.id])

    def __str__(self):
        return self.name
