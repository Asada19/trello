# Generated by Django 4.1.3 on 2022-11-27 11:31

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_comment_created_on_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None),
        ),
    ]