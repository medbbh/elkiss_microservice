# Generated by Django 5.0.1 on 2025-03-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="solde",
            field=models.FloatField(default=1000),
        ),
    ]
