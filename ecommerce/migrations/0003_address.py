# Generated by Django 5.0.3 on 2024-05-07 15:10

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_product_is_best_selling'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=300)),
                ('house_number', models.CharField(max_length=255)),
                ('city_or_town', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(max_length=746, multiple=True)),
                ('save_info', models.BooleanField(default=False)),
                ('payment_option', models.BooleanField(default=False)),
            ],
        ),
    ]
