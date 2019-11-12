from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from applications.money import models


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    pass


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency', 'sum')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'val', 'id')


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'account', 'amount', 'sum', 'info', 'date', 'created_at', 'account__sum', 'in_som')
    readonly_fields = ('created_at', )
    list_filter = ('account', 'category')
