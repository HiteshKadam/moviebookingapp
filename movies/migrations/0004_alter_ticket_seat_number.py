# Generated by Django 4.1.9 on 2023-06-24 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_ticket_seat_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='seat_number',
            field=models.CharField(error_messages={'max_length': 'Ensure this value has at most 10 characters.'}, max_length=10),
        ),
    ]
