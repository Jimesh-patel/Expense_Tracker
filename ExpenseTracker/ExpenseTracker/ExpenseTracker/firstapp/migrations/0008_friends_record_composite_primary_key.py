# Generated by Django 5.0.1 on 2024-03-29 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_remove_friends_record_gid_alter_friends_record_f_uid_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='friends_record',
            constraint=models.UniqueConstraint(fields=('uid', 'f_uid'), name='composite_primary_key'),
        ),
    ]
