# Generated by Django 3.1.7 on 2021-04-17 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_customer_registerdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
