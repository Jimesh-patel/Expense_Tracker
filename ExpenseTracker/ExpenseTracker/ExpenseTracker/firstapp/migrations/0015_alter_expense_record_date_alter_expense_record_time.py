# Generated by Django 5.0.1 on 2024-03-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0014_expense_record_date_expense_record_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_record',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='expense_record',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]
