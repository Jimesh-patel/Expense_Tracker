# Generated by Django 5.0.1 on 2024-03-30 06:37

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0019_remove_friends_record_composite_primary_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 3, 30, 12, 7, 2, 349450), null=True),
        ),
        migrations.CreateModel(
            name='Group_expense_record',
            fields=[
                ('eid', models.BigAutoField(primary_key=True, serialize=False)),
                ('total_amount', models.BigIntegerField()),
                ('splited_amount', models.BigIntegerField(null=True)),
                ('description', models.TextField(max_length=500, null=True)),
                ('date_field', models.DateField(default=datetime.date(2024, 3, 30), null=True)),
                ('time_field', models.TimeField(default=datetime.datetime(2024, 3, 30, 12, 7, 2, 350450), null=True)),
                ('gid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='firstapp.group')),
                ('payer_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Group_expense_payer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
