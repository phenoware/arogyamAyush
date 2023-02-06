# Generated by Django 4.0.1 on 2022-10-09 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_usernotifications_dealer_alter_inbox_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('review', models.TextField(default='')),
                ('date', models.CharField(default='', max_length=200)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
            ],
        ),
    ]
