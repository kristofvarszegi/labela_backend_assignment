from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User

from .constants import ORDER_STATUS_IN_CART, ORDER_STATUS_SUBMITTED

APP_LABEL = "autocompany"


class Product(models.Model):
    name = models.CharField(max_length=255)
    details = models.CharField(max_length=4095)

    class Meta:
        app_label = APP_LABEL


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Order")
    status = models.PositiveIntegerField()
    delivery_datetime = models.DateTimeField(default=None, blank=True, null=True)

    @staticmethod
    def is_delivery_datetime_valid(del_dt: datetime):
        if del_dt is None:
            return False
        # TODO ask the PO for the rule of delivery date validity and implement that
        if del_dt < (datetime.now() + timedelta(days=1)):
            return False
        return True

    def has_product(self, product_id: int):
        return OrderItem.objects.filter(
            order_id=self.id, product_id=product_id
        ).exists()

    def add_product(self, product_id: int):
        if self.status != ORDER_STATUS_IN_CART:
            raise ValueError(
                f"Cannot add product {product_id} to order {self.id}: order has already been submitted."
            )
        OrderItem.objects.create(order=self, product_id=product_id)

    def remove_product(self, product_id: int):
        if not self.has_product(product_id):
            raise ValueError(
                f"Cannot remove product {product_id} from order {self.id}: product not in order"
            )
        if self.status != ORDER_STATUS_IN_CART:
            raise ValueError(
                f"Cannot remove product {product_id} from order {self.id}: order has already been submitted"
            )
        OrderItem.objects.filter(
            order_id=self.id,
            product_id=product_id,
        ).delete()
        if not OrderItem.objects.filter(order_id=self.id).exists():
            Order.objects.filter(pk=self.id).delete()

    def set_delivery_datetime(self, del_dt):
        if Order.is_delivery_datetime_valid(del_dt):
            self.delivery_datetime = del_dt
            self.save()
        else:
            raise ValueError("Invalid delivery datetime")

    def submit(self):
        if Order.is_delivery_datetime_valid(self.delivery_datetime):
            self.status = ORDER_STATUS_SUBMITTED  # TODO ask the PO and the architect about interfacing with the payment and delivery systems
            self.save()
        else:
            raise ValueError("Invalid delivery datetime")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
