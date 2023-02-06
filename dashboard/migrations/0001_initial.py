# Generated by Django 4.0.4 on 2022-06-20 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminNotifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='', max_length=100)),
                ('msg', models.CharField(default='', max_length=500)),
                ('date', models.DateTimeField(null=True)),
                ('link', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(default='', max_length=100)),
                ('password', models.CharField(default='', max_length=100)),
                ('pins', models.IntegerField(default=10, null=True)),
                ('date', models.DateField(null=True)),
                ('walletBalance', models.IntegerField(default=0, null=True)),
                ('paidBalance', models.IntegerField(default=0, null=True)),
                ('pendingBalance', models.IntegerField(default=0, null=True)),
                ('bankName', models.CharField(default='', max_length=200)),
                ('ifscCode', models.CharField(default='', max_length=200)),
                ('accountNumber', models.CharField(default='', max_length=200)),
                ('status', models.CharField(default='Active', max_length=200)),
                ('remark', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(default='', max_length=200)),
                ('phone', models.CharField(default='', max_length=200)),
                ('name', models.CharField(default='', max_length=200)),
                ('subject', models.CharField(default='', max_length=300)),
                ('msg', models.CharField(default='', max_length=500)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='Placed', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='')),
                ('price', models.CharField(default='', max_length=200)),
                ('unit', models.CharField(default='', max_length=200)),
                ('status', models.CharField(default='available', max_length=200)),
                ('image', models.ImageField(default='', upload_to='dashboard/images/product')),
            ],
        ),
        migrations.CreateModel(
            name='UserNotifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='', max_length=100)),
                ('msg', models.CharField(default='', max_length=500)),
                ('date', models.DateTimeField(null=True)),
                ('link', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('transactionType', models.CharField(default='', max_length=300)),
                ('transactionMode', models.CharField(default='', max_length=300)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='success', max_length=200)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.dealer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('phone', models.CharField(default='', max_length=200)),
                ('name', models.CharField(default='', max_length=200)),
                ('email', models.CharField(default='', max_length=200)),
                ('transactionType', models.CharField(default='', max_length=300)),
                ('transactionMode', models.CharField(default='', max_length=300)),
                ('paymentId', models.CharField(default='', max_length=300)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='', max_length=200)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
            ],
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(default='', max_length=100)),
                ('sponseredId', models.CharField(default='', max_length=100)),
                ('date', models.DateField(null=True)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.dealer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
            ],
        ),
        migrations.AddField(
            model_name='dealer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.product'),
        ),
        migrations.AddField(
            model_name='dealer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
