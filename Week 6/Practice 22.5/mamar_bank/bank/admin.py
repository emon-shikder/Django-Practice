from django.contrib import admin
from .models import BankModel

@admin.register(BankModel)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_bankrupt')
