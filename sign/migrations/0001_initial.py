# Generated by Django 2.2.2 on 2019-06-14 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('limit', models.IntegerField()),
                ('status', models.BooleanField()),
                ('address', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField(verbose_name='events time')),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('sign', models.BooleanField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sign.Event')),
            ],
            options={
                'unique_together': {('event', 'phone')},
            },
        ),
    ]
