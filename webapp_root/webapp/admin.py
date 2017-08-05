from django.contrib import admin
from .models import Category, Ad


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date_create', 'date_update', 'active']
    list_filter = ['active']
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
