# Generated by Django 2.0.7 on 2018-07-24 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_filmparameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmparameter',
            name='rs232_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='rs232 time'),
        ),
    ]
