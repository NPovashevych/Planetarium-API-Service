# Generated by Django 5.0.4 on 2024-04-05 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0006_rename_theme_astronomyshow_themes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='astronomyshow',
            name='themes',
            field=models.ManyToManyField(blank=True, related_name='astronomy_shows', to='planetarium.showtheme'),
        ),
    ]