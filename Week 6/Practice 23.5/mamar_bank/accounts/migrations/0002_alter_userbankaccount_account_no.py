# Generated by Django 5.0.6 on 2024-10-16 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='account_no',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
