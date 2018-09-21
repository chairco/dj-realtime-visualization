# Generated by Django 2.1.1 on 2018-09-19 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('filmid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pic', models.CharField(max_length=30, verbose_name='pic')),
                ('pic_url', models.CharField(blank=True, max_length=30, null=True, verbose_name='pic_url')),
                ('cam', models.IntegerField(choices=[(0, 'CAM0'), (1, 'CAM1')], verbose_name='CAM NO.')),
                ('rs232_time', models.DateTimeField(blank=True, null=True, verbose_name='rs232_time')),
                ('len_ret', models.CharField(choices=[('0', 'FAIL'), ('1', 'PASS')], max_length=4, verbose_name='間距檢驗')),
                ('gap_ret', models.CharField(choices=[('0', 'FAIL'), ('1', 'PASS')], max_length=4, verbose_name='長度檢驗')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Film',
                'verbose_name_plural': 'Films',
                'ordering': ('create_time',),
            },
        ),
        migrations.CreateModel(
            name='FilmGap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gap0', models.FloatField(blank=True, null=True, verbose_name='左邊|粉色')),
                ('gap1', models.FloatField(blank=True, null=True, verbose_name='粉色|橘色')),
                ('gap2', models.FloatField(blank=True, null=True, verbose_name='橘色|黃色')),
                ('gap3', models.FloatField(blank=True, null=True, verbose_name='黃色|綠色')),
                ('gap4', models.FloatField(blank=True, null=True, verbose_name='綠色|藍色')),
                ('gap5', models.FloatField(blank=True, null=True, verbose_name='藍色|右邊')),
                ('film', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film_gaps', to='films.Film', verbose_name='FilmGaps')),
            ],
            options={
                'verbose_name': 'FilmGap',
                'verbose_name_plural': 'FilmGaps',
            },
        ),
        migrations.CreateModel(
            name='FilmLen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pink', models.FloatField(blank=True, null=True, verbose_name='粉色')),
                ('orange', models.FloatField(blank=True, null=True, verbose_name='橘色')),
                ('yellow', models.FloatField(blank=True, null=True, verbose_name='黃色')),
                ('green', models.FloatField(blank=True, null=True, verbose_name='綠色')),
                ('blue', models.FloatField(blank=True, null=True, verbose_name='藍色')),
                ('film', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film_lens', to='films.Film', verbose_name='FilmLens')),
            ],
            options={
                'verbose_name': 'FilmLen',
                'verbose_name_plural': 'FilmLens',
            },
        ),
        migrations.CreateModel(
            name='FilmSeq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seqid', models.UUIDField(default=uuid.uuid1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'FilmSeq',
                'verbose_name_plural': 'FilmSeqs',
                'ordering': ('create_time',),
            },
        ),
        migrations.CreateModel(
            name='FilmType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(max_length=20, verbose_name='content_type')),
            ],
            options={
                'verbose_name': 'FilmType',
                'verbose_name_plural': 'FilmTypes',
            },
        ),
        migrations.CreateModel(
            name='FilmWidth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pink', models.FloatField(blank=True, null=True, verbose_name='粉色')),
                ('orange', models.FloatField(blank=True, null=True, verbose_name='橘色')),
                ('yellow', models.FloatField(blank=True, null=True, verbose_name='黃色')),
                ('green', models.FloatField(blank=True, null=True, verbose_name='綠色')),
                ('blue', models.FloatField(blank=True, null=True, verbose_name='藍色')),
                ('film', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film_widths', to='films.Film', verbose_name='FilmWidth')),
            ],
            options={
                'verbose_name': 'FilmWidth',
                'verbose_name_plural': 'FilmWidths',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.TextField()),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='film',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='film_types', to='films.FilmType', verbose_name='FilmType'),
        ),
        migrations.AddField(
            model_name='film',
            name='seq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='film_seqs', to='films.FilmSeq', verbose_name='FilmSeqs'),
        ),
    ]
