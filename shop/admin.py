from django.contrib import admin
from shop.models import Product,Picture

class PictureInline(admin.TabularInline):
	model = Picture

class ProductAdmin(admin.ModelAdmin):
	inlines = [PictureInline, ]

admin.site.register(Product,ProductAdmin)
admin.site.register(Picture)
# Register your models here.
