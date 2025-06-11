from django.contrib import admin
from .models import Product, ProductImage, Order, OrderDetail, InventoryMovement


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = [ 'stock', 'created_at', 'updated_at' ]
    inlines = [ProductImageInline,]

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline,]


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    pass



