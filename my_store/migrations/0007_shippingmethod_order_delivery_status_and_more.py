# Generated by Django 5.0.3 on 2024-06-20 22:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0006_coupon_used_by_alter_coupon_valid_from_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_time', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('processing', 'processing'), ('in_progress', 'in_progress'), ('delivered', 'delivered')], default='Processing', max_length=255),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 20, 22, 5, 12, 922501, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 6, 20, 22, 5, 12, 922501, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 20, 23, 5, 12, 922501)),
        ),
    ]
