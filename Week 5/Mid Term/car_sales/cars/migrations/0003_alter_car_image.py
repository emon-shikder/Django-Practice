# Generated by Django 5.0.6 on 2024-09-12 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(upload_to='media/cars/'),
        ),
    ]
