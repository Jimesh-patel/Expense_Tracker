from django.contrib import admin
from firstapp.models import *


# Register your models here.
models_list = [CustomUser, Expense_record, Friends_record,  Group, Group_data, Group_expense_record] 
admin.site.register(models_list)


