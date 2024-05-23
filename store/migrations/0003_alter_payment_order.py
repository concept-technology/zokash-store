# Generated by Django 5.0.3 on 2024-05-23 01:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='store.order'),
        ),
    ]