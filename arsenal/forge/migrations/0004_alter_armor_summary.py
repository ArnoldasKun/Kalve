# Generated by Django 4.1.3 on 2022-12-07 16:23

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0003_armororder_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armor',
            name='summary',
            field=tinymce.models.HTMLField(verbose_name='summary'),
        ),
    ]
