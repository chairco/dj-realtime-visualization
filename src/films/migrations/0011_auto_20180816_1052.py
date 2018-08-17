# Generated by Django 2.1 on 2018-08-16 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0010_auto_20180801_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='gap_ret',
            field=models.CharField(choices=[('0', 'FAIL'), ('1', 'PASS')], max_length=4, verbose_name='長度檢驗'),
        ),
        migrations.AlterField(
            model_name='film',
            name='len_ret',
            field=models.CharField(choices=[('0', 'FAIL'), ('1', 'PASS')], max_length=4, verbose_name='間距檢驗'),
        ),
    ]
