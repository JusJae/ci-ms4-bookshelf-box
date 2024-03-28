# Generated by Django 3.2.23 on 2024-03-28 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_auto_20240328_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='plan',
            field=models.CharField(choices=[('basic', 'Basic (2 books)'), ('standard', 'Standard (3 books)'), ('premium', 'Premium (4 books)')], default='basic', max_length=20),
        ),
        migrations.AlterField(
            model_name='usersubscriptionoption',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscriptionplan'),
        ),
    ]
