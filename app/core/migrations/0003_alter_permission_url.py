# Generated by Django 4.0.10 on 2024-12-04 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_role_role_key_remove_role_user_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=500),
        ),
    ]