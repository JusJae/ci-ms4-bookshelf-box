# Generated by Django 3.2.23 on 2024-02-03 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionoption',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='subscriptionoption',
            name='subscription_type',
            field=models.CharField(choices=[('one-off', 'One-off'), ('three_months', '3-months'), ('six_months', '6-months'), ('twelve_months', '12-months')], max_length=20),
        ),
    ]
