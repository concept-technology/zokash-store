# Generated by Django 5.0.3 on 2024-04-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_category_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female')], default='female', max_length=10),
        ),
    ]
