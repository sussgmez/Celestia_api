from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from simple_history.models import HistoricalRecords


class Category(models.Model):
    subcategory_of = models.ForeignKey(
        "ecommerce.Category",
        verbose_name=_("Categoría"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(_("Nombre"), max_length=100)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product_color = models.ForeignKey(
        "ecommerce.ProductColor",
        verbose_name=_(""),
        on_delete=models.CASCADE,
        related_name="product_images",
    )
    image = models.ImageField(_("Imagen"), upload_to="products")

    class Meta:
        verbose_name = _("productimage")
        verbose_name_plural = _("productimages")


class Product(models.Model):
    name = models.CharField(_("Nombre"), max_length=200)
    description = models.TextField(_("Descripción"))
    category = models.ForeignKey(
        "ecommerce.Category",
        verbose_name=_("Categoría"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    price = models.FloatField(_("Precio"))
    by_size = models.BooleanField(_("¿Tiene varias tallas?"), default=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    product = models.ForeignKey(
        "ecommerce.Product", verbose_name=_("Producto"), on_delete=models.CASCADE
    )
    color = models.CharField(_("Color"), max_length=50)
    discount = models.PositiveIntegerField(
        _("Descuento"), default=0, validators=[MaxValueValidator(100)]
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Product (color)")
        verbose_name_plural = _("Products (color)")

    def __str__(self):
        return f"{self.product.name} ({self.color})"


class ProductSize(models.Model):
    product_color = models.ForeignKey(
        "ecommerce.ProductColor",
        verbose_name=_("Producto (Color)"),
        related_name="product_sizes",
        on_delete=models.CASCADE,
    )
    size = models.CharField(_("Talla"), max_length=50)
    stock = models.IntegerField(_("Stock"), default=0)

    class Meta:
        verbose_name = _("productsize")
        verbose_name_plural = _("productsizes")
        
    def __str__(self):
        return f'{self.product_color} ({self.size})'


class Bill(models.Model):
    STATUS = [
        (0, "Pendiente"),
        (1, "Aprobado"),
        (2, "Rechazado"),
    ]
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name=_("Usuario"), on_delete=models.CASCADE
    )
    status = models.IntegerField(_("Status"), choices=STATUS, default=0)


class Order(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name=_("Usuario"), on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "ecommerce.ProductSize", verbose_name=_("Producto"), on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(_("Cantidad"))
    bill = models.ForeignKey("ecommerce.Bill", verbose_name=_("Factura"), on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f'{self.user.email} | {self.product} | {self.quantity}'
    

"""
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


