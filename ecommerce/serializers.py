from rest_framework import serializers
from .models import Product, Category, ProductImage, ProductColor, ProductSize


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "price", "by_size"]



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["id", "size", "stock"]



class ProductColorSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    product_sizes = ProductSizeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductColor
        fields = ["id", "product", "color", "discount", "product_images", "product_sizes"]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "subcategory_of", "name"]
