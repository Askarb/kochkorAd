from datetime import datetime
from django.contrib import admin
from .models import Category, Ad, AdImage, Slider, Message, Variable


def ad_update(modeladmin, request, queryset):
    queryset.update(date_update=datetime.now())
ad_update.short_description = "Rise selected ads"


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
    search_fields = ('title', 'phone1', 'phone2')
    list_filter = ['is_active', 'category']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [AdImageInline, ]
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
