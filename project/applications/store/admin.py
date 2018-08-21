from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from applications.store.models import Category, Store, Goods, GoodsImage


@admin.register(Category)
class CatgoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    inlines = ()


class GoodsImageInline(AdminImageMixin, admin.TabularInline):
    model = GoodsImage
    extra = 3


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'published')
    inlines = [GoodsImageInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    prepopulated_fields = {"slug": ("name",)}


