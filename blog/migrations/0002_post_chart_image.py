# Generated by Django 4.2.17 on 2025-01-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='chart_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/charts'),
        ),
    ]
