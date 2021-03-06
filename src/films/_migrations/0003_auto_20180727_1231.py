# Generated by Django 2.0.7 on 2018-07-27 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_auto_20180727_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmgap',
            name='id',
        ),
        migrations.RemoveField(
            model_name='filmlen',
            name='id',
        ),
        migrations.RemoveField(
            model_name='filmwidth',
            name='id',
        ),
        migrations.AlterField(
            model_name='filmgap',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='film_gap', serialize=False, to='films.Film', verbose_name='Film'),
        ),
        migrations.AlterField(
            model_name='filmlen',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='film_len', serialize=False, to='films.Film', verbose_name='Film'),
        ),
        migrations.AlterField(
            model_name='filmwidth',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='film_width', serialize=False, to='films.Film', verbose_name='Film'),
        ),
    ]
