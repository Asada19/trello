# Generated by Django 4.1.3 on 2022-12-02 01:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0020_remove_board_members_alter_card_date_of_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='members',
            field=models.ManyToManyField(related_name='boards', to=settings.AUTH_USER_MODEL),
        ),
    ]
