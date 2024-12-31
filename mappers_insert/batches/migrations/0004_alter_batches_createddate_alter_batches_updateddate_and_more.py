# Generated by Django 4.2.11 on 2024-07-05 04:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "batches",
            "0003_alter_batches_createddate_alter_batches_updateddate_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="batches",
            name="CreatedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 710552), null=True
            ),
        ),
        migrations.AlterField(
            model_name="batches",
            name="UpdatedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 710552), null=True
            ),
        ),
        migrations.AlterField(
            model_name="mappersdata",
            name="CreatedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 710552), null=True
            ),
        ),
        migrations.AlterField(
            model_name="mappersdata",
            name="GMTCreatedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 726264)
            ),
        ),
        migrations.AlterField(
            model_name="mappersdata",
            name="GMTModifiedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 726264)
            ),
        ),
        migrations.AlterField(
            model_name="mappersdata",
            name="UpdatedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 710552), null=True
            ),
        ),
        migrations.AlterField(
            model_name="reporttemplates",
            name="CreatedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 710552), null=True
            ),
        ),
        migrations.AlterField(
            model_name="reporttemplates",
            name="UpdatedDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 4, 21, 33, 56, 710552), null=True
            ),
        ),
    ]
