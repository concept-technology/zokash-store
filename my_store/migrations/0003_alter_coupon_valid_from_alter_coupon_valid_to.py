# Generated by Django 5.0.3 on 2024-05-30 13:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0002_remove_order_billing_address_alter_coupon_valid_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 30, 13, 54, 56, 880635, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 30, 13, 54, 56, 880635, tzinfo=datetime.timezone.utc)),
        ),
    ]