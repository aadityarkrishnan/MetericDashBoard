# Generated by Django 4.2.16 on 2024-11-16 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Metrics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("cpu", models.FloatField()),
                ("memory", models.FloatField()),
                ("storage", models.FloatField()),
            ],
        ),
    ]
