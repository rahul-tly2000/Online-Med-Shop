# Generated by Django 4.0.3 on 2022-03-23 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_purchase_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='requested_med',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchase',
            name='verify_med',
            field=models.IntegerField(default=0),
        ),
    ]
