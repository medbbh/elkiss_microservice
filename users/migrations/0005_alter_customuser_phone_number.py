# Generated by Django 5.0.1 on 2025-03-12 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_country_allowed_prefixes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
