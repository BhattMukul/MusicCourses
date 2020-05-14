from django.contrib import admin
from .models import Instructor, Student, MoneyTransfer


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    search_fields = ['user']


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_credits', 'credits_15',
                    'age', 'created', 'bank_account_name', 'bank_name', 'bank_account_number']
    search_fields = ['username', 'first_name', 'last_name']


@admin.register(MoneyTransfer)
class MoneyTransferAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'amount', 'requested', 'transfered']
    search_fields = ['instructor', 'amount']
