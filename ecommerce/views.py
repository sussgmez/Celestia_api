from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, ProductImage, Category


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


