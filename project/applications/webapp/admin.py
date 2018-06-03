from datetime import datetime
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Category, Ad, AdImage, Slider, Message, Variable, AdPhone


def ad_update(modeladmin, request, queryset):
    queryset.update(date_update=datetime.now())
ad_update.short_description = "Rise selected ads"


class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ['pk', 'name', 'name_ru', 'name_ky', 'name_en', 'slug']
    list_display_links = ('pk', 'name')
    prepopulated_fields = {"slug": ("name",)}


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 3


class AdPhoneInline(admin.TabularInline):
    model = AdPhone
    extra = 3


class AdAdmin(admin.ModelAdmin):

    actions_on_top = True
    save_on_top = True
    list_display = ['title', 'category', 'date_create', 'date_update', 'is_active',
                    'rise_count', 'view_count']
    search_fields = ('title',)
    list_filter = ['is_active', 'category']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [AdPhoneInline, AdImageInline, ]
    list_editable = ['is_active']
    actions = [ad_update]


class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'priority')
    list_editable = ('active', 'priority')


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    readonly_fields = ('name', )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'phone', 'message')
    list_display_links = ('pk', 'name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Slider, SliderAdmin)
