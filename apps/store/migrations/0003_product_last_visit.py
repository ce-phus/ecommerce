# Generated by Django 5.0.6 on 2024-06-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_product_last_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_visit',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]