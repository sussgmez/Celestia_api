from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(_("Categoría"), max_length=50)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("Nombre"), max_length=200)
    description = models.TextField(_("Descripción"), blank=True, null=True)
    price = models.FloatField(_("Precio"), validators=[MinValueValidator(0.0)])
    discount = models.FloatField(_("Descuento"), default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    category = models.ForeignKey("ecommerce.Category", verbose_name=_("Categoría"), on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Última modificación"), auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return f'ID #{self.id}'


class ProductImage(models.Model):
    product = models.ForeignKey("ecommerce.Product", verbose_name=_("Producto"), on_delete=models.CASCADE)
    image = models.ImageField(_("Imagen"), upload_to='ecommerce/products/')
    
    class Meta:
        verbose_name = _("productimage")
        verbose_name_plural = _("productimages")

    def __str__(self):
        return f'{self.product.name} ({self.id})' 


class ProductSize(models.Model):
    size = models.CharField(_("Talla"), max_length=50)

    def __str__(self):
        return self.size
    
class ProductColor(models.Model):
    color = models.CharField(_("Color"), max_length=50)

    def __str__(self):
        return self.color


class ProductInventory(models.Model):
    product = models.ForeignKey("ecommerce.Product", verbose_name=_("Product"), on_delete=models.CASCADE)
    size = models.ForeignKey("ecommerce.ProductSize", verbose_name=_(""), on_delete=models.CASCADE)
    color = models.ForeignKey("ecommerce.ProductColor", verbose_name=_(""), on_delete=models.CASCADE)
    stock = models.IntegerField(_("Cantidad"), validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.product.name} Talla: {self.size} Color: {self.color}'

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Cliente"), on_delete=models.CASCADE)
    date = models.DateTimeField(_("Fecha"), auto_now_add=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f'{self.id} - {self.user} - {self.date.strftime('%x %X')}'


class OrderDetail(models.Model):
    order = models.ForeignKey("ecommerce.Order", verbose_name=_("Orden"), on_delete=models.CASCADE)
    product_inventory = models.ForeignKey("ecommerce.ProductInventory", verbose_name=_("Producto"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("Cantidad"), validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _("orderdetail")
        verbose_name_plural = _("order details")

    def __str__(self):
        return f'{self.order.id}.{self.id} - {self.order.user} - {self.product_inventory} - {self.quantity}'
    

@receiver(pre_save, sender=OrderDetail)
def order_detail_pre_save_receiver(sender, instance: OrderDetail, **kwargs):
    if instance.pk is None:
        if instance.quantity > instance.product_inventory.stock:
            raise ValidationError('Cantidad no disponible')
        else:
            instance.product_inventory.stock -= instance.quantity
            instance.product_inventory.save()
    else:
        quantity = instance.quantity - OrderDetail.objects.get(id=instance.id).quantity
        if quantity > instance.product_inventory.stock:
            raise ValidationError('Cantidad no disponible')
        else:
            instance.product_inventory.stock -= quantity
            instance.product_inventory.save()

@receiver(pre_delete, sender=OrderDetail)
def order_detail_pre_delete_receiver(sender, instance: OrderDetail, **kwargs):
    instance.product_inventory.stock += instance.quantity
    instance.product_inventory.save()

"""
@receiver(pre_save, sender=OrderDetail)
def order_detail_pre_save_receiver(sender, instance, **kwargs):
    if instance.pk is None:
        if instance.quantity > instance.product.stock:
            raise ValidationError('Cantidad no disponible')
        else:
            instance.product.stock-= instance.quantity
            instance.product.save()
    else:
        quantity = instance.quantity - OrderDetail.objects.get(id=instance.id).quantity 
        if quantity > instance.product.stock:
            raise ValidationError('Cantidad no disponible')
        else:
            instance.product.stock-= quantity
            instance.product.save()


@receiver(pre_delete, sender=OrderDetail)
def order_detail_pre_delete_receiver(sender, instance, **kwargs):
    instance.product.stock += instance.quantity
    instance.product.save()
"""