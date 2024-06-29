# Generated by Django 5.0.6 on 2024-06-29 07:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_last_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='last_visit',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]