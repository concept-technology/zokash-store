# Generated by Django 5.0.3 on 2024-04-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female')], default='female', max_length=10),
        ),
    ]
