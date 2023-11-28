# Generated by Django 4.1.12 on 2023-10-26 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Candidate",
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
                ("first_name", models.CharField(default="John", max_length=255)),
                ("last_name", models.CharField(default="Doe", max_length=255)),
                ("party_name", models.CharField(default="NOTA", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Election",
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
                ("name", models.CharField(default="No Data", max_length=255)),
                ("candidates", models.ManyToManyField(to="base.candidate")),
            ],
        ),
        migrations.CreateModel(
            name="Vote",
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
                ("voter_id", models.CharField(default="No Data", max_length=255)),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.candidate"
                    ),
                ),
                (
                    "election",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.election"
                    ),
                ),
            ],
        ),
    ]
