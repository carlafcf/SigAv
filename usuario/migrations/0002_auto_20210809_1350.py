# Generated by Django 3.1.7 on 2021-08-09 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ['is_active', 'first_name', 'last_name']},
        ),
    ]