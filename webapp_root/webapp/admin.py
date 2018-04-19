from django.contrib import admin
from .models import Category, Ad, AdImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1


class AdAdmin(admin.ModelAdmin):

    actions_on_top = True
    save_on_top = True
    list_display = ['title', 'category', 'date_create', 'phone1', 'phone2', 'is_active',
                    'rise_count', 'view_count']
    # list_filter = ['is_active']
    # prepopulated_fields = {"slug": ("title",)}
    # inlines = [AdImageInline, ]
    # list_editable = ['is_active']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
