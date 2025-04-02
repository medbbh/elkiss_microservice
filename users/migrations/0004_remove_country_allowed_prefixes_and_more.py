# Generated by Django 5.0.1 on 2025-03-12 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_country_alter_customuser_phone_number_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="country",
            name="allowed_prefixes",
        ),
        migrations.RemoveField(
            model_name="country",
            name="country_code",
        ),
        migrations.AddField(
            model_name="country",
            name="iso_code",
            field=models.CharField(default="MR", max_length=2, unique=True),
            preserve_default=False,
        ),
    ]
