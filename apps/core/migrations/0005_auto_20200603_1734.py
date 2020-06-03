# Generated by Django 2.2 on 2020-06-03 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_tool_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='tools',
        ),
        migrations.CreateModel(
            name='Toolset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='name')),
                ('toolset_type', models.IntegerField(choices=[(1, 'graphic art'), (2, 'pictorial art'), (3, 'mixed art')], db_index=True, verbose_name='toolset type')),
                ('tools', models.ManyToManyField(blank=True, db_index=True, to='core.Tool', verbose_name='tools')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='toolset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Toolset', verbose_name='toolset'),
        ),
    ]
