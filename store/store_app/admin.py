from django.contrib import admin

from .models import *


class ImageAdminStack(admin.StackedInline):
    model = Image


class SizesAdminStack(admin.StackedInline):
    model = Sizes

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdminStack, SizesAdminStack]
    list_display = ( 'name', 'price', 'cost', 'in_stock' ,'is_active', 'get_sizes_stock' )
    prepopulated_fields = { 'slug': ('name',) }

    class Meta:
        model = Product

class ImageAdmin(admin.ModelAdmin):

    list_display = ('image', 'product')

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
