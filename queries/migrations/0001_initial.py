# Generated by Django 5.0.6 on 2024-06-14 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=35)),
                ('ph_no', models.CharField(default='', max_length=15)),
                ('subject', models.CharField(max_length=100)),
                ('msg', models.CharField(default='', max_length=600)),
                ('timestamp', models.DateTimeField()),
                ('answered', models.BooleanField(default=False)),
            ],
        ),
    ]
