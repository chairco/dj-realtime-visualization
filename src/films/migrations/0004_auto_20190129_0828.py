# Generated by Django 2.1 on 2019-01-29 00:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_auto_20190128_1718'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='film',
            name='films_film_sv_63e1cd_gin',
        ),
        migrations.RemoveField(
            model_name='film',
            name='sv',
        ),
        migrations.AlterField(
            model_name='film',
            name='filmid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
