# Generated by Django 5.0.6 on 2024-06-23 17:14

import datetime
import django.core.validators
import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature1', models.CharField(blank=True, max_length=255, null=True)),
                ('feature2', models.CharField(blank=True, max_length=255, null=True)),
                ('feature3', models.CharField(blank=True, max_length=255, null=True)),
                ('feature4', models.CharField(blank=True, max_length=255, null=True)),
                ('feature5', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_time', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('is_ordered', models.BooleanField(default=False)),
                ('session', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('amount', models.IntegerField(default=0)),
                ('valid_from', models.DateTimeField(default=datetime.datetime(2024, 6, 23, 17, 14, 38, 619225, tzinfo=datetime.timezone.utc))),
                ('valid_to', models.DateTimeField(blank=True, default=datetime.datetime(2024, 6, 23, 17, 14, 38, 619225, tzinfo=datetime.timezone.utc), null=True)),
                ('active', models.BooleanField(default=True)),
                ('is_used', models.BooleanField(default=False)),
                ('used_by', models.ManyToManyField(blank=True, related_name='used_coupons', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomersAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=300)),
                ('apartment', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('telephone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('zip_code', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('payment_option', models.CharField(blank=True, choices=[('paypal', 'paypal'), ('paystack', 'paystack')], max_length=255, null=True)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('ref', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False)),
                ('reference', models.CharField(default='', max_length=50)),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_received', models.BooleanField(default=False)),
                ('is_refund_request', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2024, 6, 23, 18, 14, 38, 619225))),
                ('delivery_status', models.CharField(choices=[('processing', 'processing'), ('in_progress', 'in_progress'), ('delivered', 'delivered')], default='Processing', max_length=255)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_store.coupon')),
                ('product', models.ManyToManyField(to='my_store.cart')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_store.customersaddress')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='my_store.payment')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1000)),
                ('additional_information', models.TextField(default='', max_length=1000)),
                ('size', models.CharField(choices=[('500ml', '500ml'), ('25ml', '25ml'), ('1L', '1L'), ('4L', '4L'), ('10L', '10L'), ('25L', '25L')], default='1L', max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('discount_price', models.IntegerField(default=0)),
                ('img_1', models.ImageField(default='img', upload_to='static/media/img')),
                ('img_2', models.ImageField(blank=True, default='img', null=True, upload_to='static/media/img')),
                ('img_3', models.ImageField(blank=True, default='img', null=True, upload_to='static/media/img')),
                ('img_4', models.ImageField(blank=True, default='img', null=True, upload_to='static/media/img')),
                ('label', models.CharField(blank=True, choices=[('new', 'label-new'), ('out', 'label-out'), ('top', 'label-top'), ('sale', 'label-sale')], default='', max_length=255)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'male'), ('Female', 'female')], default='female', max_length=10, null=True)),
                ('display_on_home_page', models.BooleanField(default=False)),
                ('is_banner', models.BooleanField(default=False)),
                ('is_best_selling', models.BooleanField(default=False)),
                ('slug', models.SlugField(default='eg-product-title', unique=True)),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_store.category')),
                ('features', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_store.features')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store.product'),
        ),
        migrations.CreateModel(
            name='Refunds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(default='')),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store.order')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='my_store.product')),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]
