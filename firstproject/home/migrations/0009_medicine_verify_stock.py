# Generated by Django 4.0.3 on 2022-03-23 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_medicine_requested_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='verify_stock',
            field=models.IntegerField(default=0),
        ),
    ]