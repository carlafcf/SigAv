# Generated by Django 3.1.7 on 2021-02-19 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='quantidade_final',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]