# Generated by Django 4.0.1 on 2022-10-29 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='productName',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='qnt',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]