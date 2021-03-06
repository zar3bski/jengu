# Generated by Django 2.2 on 2019-04-29 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Unpayed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('january', models.IntegerField(default=0)),
                ('february', models.IntegerField(default=0)),
                ('march', models.IntegerField(default=0)),
                ('april', models.IntegerField(default=0)),
                ('may', models.IntegerField(default=0)),
                ('june', models.IntegerField(default=0)),
                ('july', models.IntegerField(default=0)),
                ('august', models.IntegerField(default=0)),
                ('september', models.IntegerField(default=0)),
                ('october', models.IntegerField(default=0)),
                ('november', models.IntegerField(default=0)),
                ('december', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Revenues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('january', models.FloatField(default=0.0)),
                ('february', models.FloatField(default=0.0)),
                ('march', models.FloatField(default=0.0)),
                ('april', models.FloatField(default=0.0)),
                ('may', models.FloatField(default=0.0)),
                ('june', models.FloatField(default=0.0)),
                ('july', models.FloatField(default=0.0)),
                ('august', models.FloatField(default=0.0)),
                ('september', models.FloatField(default=0.0)),
                ('october', models.FloatField(default=0.0)),
                ('november', models.FloatField(default=0.0)),
                ('december', models.FloatField(default=0.0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('birth_date', models.DateField()),
                ('inscription', models.DateTimeField(auto_now_add=True)),
                ('tel', models.CharField(max_length=20, null=True)),
                ('mail', models.CharField(max_length=80, null=True)),
                ('notes', models.TextField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Consultations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('date', models.DateTimeField()),
                ('payed', models.FloatField(null=True)),
                ('fk_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jengu.Patients')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
