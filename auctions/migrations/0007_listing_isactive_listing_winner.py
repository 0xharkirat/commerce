# Generated by Django 4.1.4 on 2022-12-23 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="isActive",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="won",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
