# Generated by Django 5.1.2 on 2024-10-30 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brrrgrrr', '0003_alter_customburger_ingredients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customburger',
            name='ingredients',
        ),
    ]