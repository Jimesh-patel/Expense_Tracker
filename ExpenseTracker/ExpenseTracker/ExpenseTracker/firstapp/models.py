from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime

# Create your models here.

class CustomUser(AbstractUser):
    uid                 = models.BigAutoField(primary_key=True)
    username            = models.CharField(max_length=100, unique=True)
    password            = models.CharField(max_length=50)
    email               = models.EmailField(verbose_name="email", max_length=100, unique=True)
    phone_no            = models.CharField(max_length=12, null = True)
    total_balance       = models.BigIntegerField(default=0)

    def __str__(self):
        return self.username
    


class Group(models.Model):
    gid                 = models.BigAutoField(primary_key=True)
    uid                 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gname               = models.CharField(max_length=100, unique=True)
    


class Expense_record(models.Model):
    eid                 = models.BigAutoField(primary_key=True)
    payer_uid           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Expense_user')
    shared_uid          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='Expense_shared_with_friend', null = True)
    total_amount        = models.BigIntegerField()
    splited_amount      = models.BigIntegerField(null = True)
    description         = models.TextField(max_length=500, null=True)
    date_field          = models.DateField( null = True, default=datetime.date.today())
    time_field          = models.TimeField( null = True, default=datetime.datetime.now())



class Friends_record(models.Model):
    id                  = models.AutoField(primary_key=True, default=None)
    uid                 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    f_uid               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_releted_to_user', default = None)
    owe_amount          = models.BigIntegerField(default=0)

    class Meta:
        # Define the composite primary key
        constraints = [
            models.UniqueConstraint(fields=['uid', 'f_uid'], name='friends_composite_primary_key')
        ]



class Group_data(models.Model):
    gid                 = models.ForeignKey(Group, on_delete=models.CASCADE)
    mid                 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        # Define the composite primary key
        constraints = [
            models.UniqueConstraint(fields=['gid', 'mid'], name='group_data_composite_primary_key')
        ]


class Group_expense_record(models.Model):
    eid                 = models.BigAutoField(primary_key=True)
    payer_uid           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Group_expense_payer')
    gid                 = models.ForeignKey(Group, on_delete=models.SET_NULL, null = True)
    total_amount        = models.BigIntegerField()
    splited_amount      = models.BigIntegerField(null = True)
    description         = models.TextField(max_length=500, null=True)
    date_field          = models.DateField( null = True, default=datetime.date.today())
    time_field          = models.TimeField( null = True, default=datetime.datetime.now())

