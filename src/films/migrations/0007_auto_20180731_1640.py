# Generated by Django 2.0.7 on 2018-07-31 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0006_auto_20180730_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='gap_ret',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='film',
            name='len_ret',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='filmlen',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film_lens', to='films.Film', verbose_name='FilmLens'),
        ),
        migrations.AlterField(
            model_name='filmwidth',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film_widths', to='films.Film', verbose_name='FilmWidth'),
        ),
    ]
