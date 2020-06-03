from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import SET_NULL
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from apps.artoolbox_auth.models import ArtoolboxUser


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
        (PENCIL, _('pencil')),
        (PEN, _('pen')),
        (BRUSH, _('brush')),
        (PAINT, _('paint')),
        (PASTEL, _('pastel')),
        (CHARCOAL, _('charcoal')),
    )

    name = models.CharField(max_length=64, db_index=True, verbose_name=_('name'))
    tool_type = models.IntegerField(choices=TYPE_CHOICES, db_index=True, verbose_name=_('tool type'))
    materials = models.ManyToManyField(Material, db_index=True, verbose_name=_('materials'), blank=True)
    description = models.TextField(blank=True, db_index=True, verbose_name=_('description'))

    def __str__(self):
        return self.name

    def get_materials(self):
        return ', '.join([material.name for material in self.materials.all()])


class Toolset(models.Model):
    GRAPHIC_ART = 1
    PICTORIAL_ART = 2
    MIXED_ART = 3

    TYPE_CHOICES = (
        (GRAPHIC_ART, _('graphic art')),
        (PICTORIAL_ART, _('pictorial art')),
        (MIXED_ART, _('mixed art')),
    )

    name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name=_('name'))
    toolset_type = models.IntegerField(choices=TYPE_CHOICES, db_index=True, verbose_name=_('toolset type'))
    tools = models.ManyToManyField(Tool, db_index=True, verbose_name=_('tools'), blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name=_('name'))
    artist = models.CharField(max_length=64, blank=True, db_index=True, verbose_name=_('artist'))
    file = models.ImageField(db_index=True, verbose_name=_('file'))
    colours = ArrayField(models.CharField(max_length=7), blank=True, db_index=True, verbose_name=_('colours'))
    description = models.TextField(blank=True, db_index=True, verbose_name=_('description'))
    user = models.ForeignKey(ArtoolboxUser, verbose_name=_('user'), blank=True, null=True, on_delete=SET_NULL)
    toolset = models.ForeignKey(Toolset, db_index=True, verbose_name=_('toolset'), blank=True, null=True,
                                on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse_lazy('core:image_detail', args=[self.id])

    def __str__(self):
        return self.name
