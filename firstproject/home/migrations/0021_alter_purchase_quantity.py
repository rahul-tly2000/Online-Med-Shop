# Generated by Django 4.0 on 2022-04-11 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_purchase_is_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
