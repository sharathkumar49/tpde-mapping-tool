# Generated by Django 4.2.11 on 2024-07-04 07:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("masters", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Batches",
            fields=[
                (
                    "CreatedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690),
                        null=True,
                    ),
                ),
                (
                    "UpdatedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690),
                        null=True,
                    ),
                ),
                ("Active", models.BooleanField(default=True)),
                ("BatchID", models.BigAutoField(primary_key=True, serialize=False)),
                ("BatchNo", models.CharField(max_length=255, unique=True)),
                (
                    "Status",
                    models.CharField(
                        choices=[
                            ("0", "Waiting For Approval"),
                            ("1", "Approved"),
                            ("2", "Rejected"),
                            ("3", "Completed"),
                        ],
                        default=0,
                        max_length=255,
                    ),
                ),
                ("ApprovedAt", models.DateTimeField(null=True)),
                ("RejectedAt", models.DateTimeField(null=True)),
                ("CompletedAt", models.DateTimeField(null=True)),
                ("RejectReason", models.TextField(null=True)),
                ("RecordCount", models.CharField(max_length=100)),
                (
                    "ApprovedBy",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "CompletedBy",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "CreatedID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "FeedCategoryID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="masters.feedcategory",
                    ),
                ),
                (
                    "FeedID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="masters.feeds"
                    ),
                ),
                (
                    "RejectedBy",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "UpdatedID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ReportTemplates",
            fields=[
                (
                    "CreatedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690),
                        null=True,
                    ),
                ),
                (
                    "UpdatedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690),
                        null=True,
                    ),
                ),
                ("Active", models.BooleanField(default=True)),
                ("TemplateID", models.BigAutoField(primary_key=True, serialize=False)),
                ("TemplateHeaders", models.TextField()),
                ("ReportHeaders", models.TextField()),
                ("TableName", models.CharField(max_length=255, null=True)),
                (
                    "CreatedID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "FeedCategoryID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="masters.feedcategory",
                    ),
                ),
                (
                    "FeedID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="masters.feeds"
                    ),
                ),
                (
                    "UpdatedID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MappersData",
            fields=[
                (
                    "CreatedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690),
                        null=True,
                    ),
                ),
                (
                    "UpdatedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690),
                        null=True,
                    ),
                ),
                ("Active", models.BooleanField(default=True)),
                ("MappingID", models.BigAutoField(primary_key=True, serialize=False)),
                ("ClientID", models.CharField(max_length=255)),
                ("BurgissPortfolioName", models.CharField(max_length=255)),
                ("UploadValuations", models.CharField(max_length=255)),
                ("PrimaryScope", models.CharField(max_length=255)),
                ("UploadTransactions", models.CharField(max_length=255)),
                ("InvestmentName", models.CharField(max_length=255)),
                ("InvestmentGUID", models.TextField()),
                ("InvestmentID", models.CharField(max_length=255)),
                ("UserPortfolioID", models.CharField(max_length=255)),
                ("PortfolioCode", models.CharField(max_length=255)),
                ("PortfolioName", models.CharField(max_length=255)),
                ("PrimaryUserFundID", models.CharField(max_length=255)),
                ("PrimaryFundName", models.CharField(max_length=255)),
                ("PrimaryFundCode", models.CharField(max_length=255)),
                ("PrimaryFundType", models.CharField(max_length=255)),
                ("EntityType", models.CharField(max_length=255)),
                ("EntryType", models.CharField(max_length=255)),
                ("CommitmentID", models.CharField(max_length=255)),
                ("ClassID", models.CharField(max_length=255)),
                ("TrancheID", models.CharField(max_length=255)),
                ("SecondaryLegCode", models.CharField(max_length=255)),
                ("SecondaryLegScope", models.CharField(max_length=255)),
                ("FundCurrency", models.CharField(max_length=255)),
                ("DuplicateEntry", models.CharField(max_length=255)),
                ("Notes", models.CharField(max_length=255)),
                (
                    "GMTCreatedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690)
                    ),
                ),
                (
                    "GMTModifiedDate",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 4, 0, 13, 24, 571690)
                    ),
                ),
                ("ErrorMessages", models.JSONField()),
                ("Error", models.BooleanField()),
                (
                    "BatchID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="batches.batches",
                    ),
                ),
                (
                    "CreatedID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "UpdatedID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
