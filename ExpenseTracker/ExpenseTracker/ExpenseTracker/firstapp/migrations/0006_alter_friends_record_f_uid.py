# Generated by Django 5.0.1 on 2024-03-28 18:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_alter_friends_record_gid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends_record',
            name='f_uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend_releted_to_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
