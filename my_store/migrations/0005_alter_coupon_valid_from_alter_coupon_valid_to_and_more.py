# Generated by Django 5.0.3 on 2024-05-31 16:19

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0004_alter_coupon_valid_from_alter_coupon_valid_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 16, 19, 44, 428792, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 16, 19, 44, 428792, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store.product')),
            ],
        ),
    ]