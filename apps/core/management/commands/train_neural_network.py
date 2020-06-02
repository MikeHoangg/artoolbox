from django.core.management import BaseCommand
from apps.core.neural_network import *

from apps.core.models import Image


class Command(BaseCommand):

    def handle(self, *args, **options):
        colours = []
        tools = []
        for image in Image.objects.all():
            colours.append(image.colours)
            tools.append(list(image.tools.values_list('id', flat=True)))

        model.fit(colours, tools, epochs=5)
