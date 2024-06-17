# Generated by Django 5.0.6 on 2024-06-14 16:19

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('name', models.CharField(max_length=35)),
                ('features', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.image')),
            ],
        ),
        migrations.CreateModel(
            name='BrandImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.brand')),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.image')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('features', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=35)),
                ('quantity', models.IntegerField()),
                ('top_featured', models.BooleanField()),
                ('datasheet', models.CharField(max_length=50)),
                ('brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.brand')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.image')),
                ('pro_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.image')),
                ('pro_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
