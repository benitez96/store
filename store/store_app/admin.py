from django.contrib import admin

from .models import *


class ImageAdminStack(admin.StackedInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdminStack]
    list_display = ( 'name', 'price', 'cost', 'stock', 'is_active' )

    class Meta:
        model = Product

class ImageAdmin(admin.ModelAdmin):

    list_display = ('image', 'product')

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)