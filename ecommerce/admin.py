from django.contrib import admin
from .models import Product, ProductColor, ProductSize, ProductImage, Category, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

class ProductColorInline(admin.TabularInline):
    model = ProductColor

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorInline]

class ProductSizeInline(admin.StackedInline):
    model = ProductSize

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline, ProductImageInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
