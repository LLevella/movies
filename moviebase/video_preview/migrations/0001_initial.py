# Generated by Django 3.1.5 on 2021-01-09 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0002_auto_20210108_0333'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoviePlayer',
            fields=[
                ('movie_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='movies.movie')),
                ('pointer', models.SmallIntegerField(default=0, verbose_name='Указатель на смещение')),
            ],
            bases=('movies.movie',),
        ),
    ]