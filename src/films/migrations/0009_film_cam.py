# Generated by Django 2.0.7 on 2018-08-01 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0008_auto_20180731_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='cam',
            field=models.IntegerField(choices=[(0, 'CAM0'), (1, 'CAM1')], default=1, max_length=1, verbose_name='CAM NO.'),
            preserve_default=False,
        ),
    ]