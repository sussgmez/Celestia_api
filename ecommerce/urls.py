from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, CategoryViewSet, ProductColorViewSet,ProductImageViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('product_colors', ProductColorViewSet)
router.register('product_images', ProductImageViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
