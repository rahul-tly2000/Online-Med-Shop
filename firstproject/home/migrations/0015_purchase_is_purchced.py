# Generated by Django 4.0.3 on 2022-03-23 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_purchase_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='is_purchced',
            field=models.BooleanField(default=False),
        ),
    ]