# Generated by Django 5.0.4 on 2024-04-05 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0005_alter_astronomyshow_theme'),
    ]

    operations = [
        migrations.RenameField(
            model_name='astronomyshow',
            old_name='theme',
            new_name='themes',
        ),
    ]
