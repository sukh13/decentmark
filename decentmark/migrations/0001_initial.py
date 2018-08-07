# Generated by Django 2.1 on 2018-08-07 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('description', models.TextField()),
                ('attempts', models.IntegerField(default=-1)),
                ('test', models.TextField()),
                ('solution', models.TextField()),
                ('template', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_class', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('solution', models.TextField()),
                ('marked', models.BooleanField(default=False)),
                ('mark', models.IntegerField(default=-1)),
                ('total', models.IntegerField(default=-1)),
                ('feedback', models.TextField(blank=True, default='')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decentmark.Assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('description', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UnitUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.BooleanField(default=False)),
                ('mark', models.BooleanField(default=False)),
                ('submit', models.BooleanField(default=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decentmark.Unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Unit User',
                'verbose_name_plural': 'Unit Users',
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decentmark.Unit'),
        ),
    ]
