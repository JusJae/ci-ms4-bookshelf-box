# Generated by Django 3.2.23 on 2024-06-08 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_auto_20240531_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionoption',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
