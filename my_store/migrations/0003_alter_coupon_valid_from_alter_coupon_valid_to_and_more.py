# Generated by Django 5.0.6 on 2024-07-06 15:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0002_alter_coupon_valid_from_alter_coupon_valid_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 6, 15, 44, 10, 48945, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 6, 15, 44, 10, 48945, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 6, 16, 44, 10, 48945)),
        ),
    ]
