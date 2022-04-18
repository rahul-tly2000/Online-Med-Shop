# Generated by Django 4.0.3 on 2022-03-23 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_user_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('income', models.IntegerField(null=True)),
                ('discription', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
