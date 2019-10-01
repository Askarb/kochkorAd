from django.contrib import admin

from applications.money import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency', 'sum')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'account', 'amount', 'sum', 'info', 'date', 'created_at', 'account__sum')
    readonly_fields = ('created_at', )
