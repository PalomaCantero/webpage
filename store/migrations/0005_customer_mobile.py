# Generated by Django 3.1.7 on 2021-04-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=30, null=True),
        ),
    ]