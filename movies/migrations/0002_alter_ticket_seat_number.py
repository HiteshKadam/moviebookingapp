# Generated by Django 4.1.9 on 2023-06-24 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='seat_number',
            field=models.CharField(error_messages={'length': 'Ensure this value has at most 10 characters.'}, max_length=10),
        ),
    ]