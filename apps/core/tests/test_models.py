from django.test import TestCase
from django.urls import reverse_lazy

from apps.core.models import Image, Tool, Material


class ModelsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Material.objects.create(
            name='test material',
            characteristics='test characteristics'
        )

        Tool.objects.create(
            name='test material',
            tool_type=Tool.PENCIL
        )

        Image.objects.create(
            name='test image',
            artist='test artist',
            colours=['#000000', '#ffffff'],
            description='test description'
        )

    def setUp(self):
        self.image = Image.objects.first()
        self.tool = Tool.objects.first()
        self.material = Material.objects.first()
        self.tool.materials.add(self.material)
        self.image.tools.add(self.tool)

    def test_relations(self):
        self.assertIn(self.tool, self.image.tools.all())
        self.assertIn(self.material, self.tool.materials.all())

    def test_get_absolute_url(self):
        self.assertEqual(reverse_lazy('core:image_detail', args=[self.image.id]), self.image.get_absolute_url())

    def test_str_method(self):
        self.assertEqual(str(self.image), self.image.name)

    def test_update_object_data(self):
        updated_data = {
            'name': 'test name',
            'artist': 'test artist'
        }

        for key, value in updated_data.items():
            setattr(self.image, key, value)
        self.image.save()
        self.assertEqual(self.image.name, updated_data['name'])
        self.assertEqual(self.image.artist, updated_data['artist'])
