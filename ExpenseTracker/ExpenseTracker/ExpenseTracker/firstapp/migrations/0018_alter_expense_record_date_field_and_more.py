# Generated by Django 5.0.1 on 2024-03-29 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0017_alter_expense_record_date_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_record',
            name='date_field',
            field=models.DateField(default=datetime.date(2024, 3, 29), null=True),
        ),
        migrations.AlterField(
            model_name='expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 3, 29, 23, 24, 0, 379156), null=True),
        ),
    ]
