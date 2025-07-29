from rest_framework import serializers
from .models import Product, Category, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "price", "by_size"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "subcategory_of", "name"]


