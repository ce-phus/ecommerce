# Generated by Django 5.0.6 on 2024-06-29 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_last_visit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='last_visit',
        ),
    ]