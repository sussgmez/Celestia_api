from django.contrib import admin
from .models import Product, ProductImage, ProductInventory, Order, OrderDetail, Category, ProductSize, ProductColor, CarouselImage


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductInventoryInline(admin.TabularInline):
    model = ProductInventory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = [ 'created_at', 'updated_at' ]
    inlines = [ProductImageInline, ProductInventoryInline]

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline,]

