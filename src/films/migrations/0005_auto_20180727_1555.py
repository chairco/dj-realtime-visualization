# Generated by Django 2.0.7 on 2018-07-27 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_auto_20180727_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmlen',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filmwidth',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filmlen',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film_len', to='films.Film', verbose_name='Film'),
        ),
        migrations.AlterField(
            model_name='filmwidth',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film_width', to='films.Film', verbose_name='Film'),
        ),
    ]