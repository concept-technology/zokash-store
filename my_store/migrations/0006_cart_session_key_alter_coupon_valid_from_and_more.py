# Generated by Django 5.0.6 on 2024-07-07 19:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0005_alter_coupon_valid_from_alter_coupon_valid_to_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 7, 19, 51, 12, 914804, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 7, 19, 51, 12, 914804, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 7, 20, 51, 12, 914804)),
        ),
    ]
