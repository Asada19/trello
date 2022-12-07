# Generated by Django 4.1.3 on 2022-11-24 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_checklist_alter_column_options_remove_board_favorite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archiwe',
            name='space',
        ),
        migrations.AddField(
            model_name='archiwe',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boards.board'),
        ),
    ]
