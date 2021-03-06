# Generated by Django 2.0.7 on 2018-07-05 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='battery_life',
            field=models.IntegerField(default=100, verbose_name='電量(%)'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(max_length=50, verbose_name='設備類型'),
        ),
        migrations.AlterField(
            model_name='device',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='經度'),
        ),
        migrations.AlterField(
            model_name='device',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='緯度'),
        ),
        migrations.AlterField(
            model_name='device',
            name='mac',
            field=models.CharField(max_length=50, unique=True, verbose_name='MAC Address'),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(default='-', max_length=50, verbose_name='設備名稱'),
        ),
        migrations.AlterField(
            model_name='device',
            name='online',
            field=models.NullBooleanField(default=None, verbose_name='線上狀態'),
        ),
    ]
