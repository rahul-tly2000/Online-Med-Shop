# Generated by Django 4.0 on 2022-04-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_rename_is_requested_med_purchase_is_requested_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='is_reject',
            field=models.BooleanField(default=False),
        ),
    ]
