import json
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User

APP_LABEL = "autocompany"

ID_LABEL = "id"
DETAILS_LABEL = "details"
NAME_LABEL = "name"


class Product(models.Model):
    name = models.CharField(max_length=255)
    details = models.CharField(max_length=4095)

    class Meta:
        app_label = APP_LABEL


ORDER_STATUS_IN_CART = 0
ORDER_STATUS_SUBMITTED = 1
ORDER_STATUS_EN_ROUTE = 2
ORDER_STATUS_DELIVERED = 3


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Order")
    status = models.PositiveIntegerField()
    delivery_datetime = models.DateTimeField(default=None, blank=True, null=True)

    def has_product(self, product_id: int):
        return OrderItem.objects.filter(
            order_id=self.id, product_id=product_id
        ).exists()

    def add_product(self, product_id: int):
        if self.status != ORDER_STATUS_IN_CART:
            raise ValueError(
                f"Cannot add product {product_id} to order {self.id}: order has already been submitted."
            )  # TODO find a more exact error type for this case
        OrderItem.objects.create(order=self, product_id=product_id)

    """def remove_product(self, product: Product):
        if self.status != ORDER_STATUS_IN_CART:
            raise ValueError(
                f"Cannot remove product {product} from order {self.id}: order has already been submitted"
            )  # TODO find a more exact error type for this case
        OrderItem.objects.delete(
            customer_id__eq=self.customer_id,
            status__eq=ORDER_STATUS_IN_CART,
            product_id__eq=product.id,
        )

    @staticmethod
    def is_delivery_datetime_valid(del_dt: datetime):
        if del_dt is None:
            return False
        if del_dt < (
            datetime.now() + timedelta(d=1)
        ):  # TODO ask the PO for the rule of delivery date validity and implement that
            return False
        return True

    def set_delivery_datetime(self, del_dt):
        if Order.is_delivery_datetime_valid(del_dt):
            self.delivery_datetime = del_dt
        else:
            # TODO
            pass

    def submit(self):
        if Order.is_delivery_datetime_valid(self.delivery_datetime):
            self.status = ORDER_STATUS_SUBMITTED  # TODO ask the PO and the architect about interfacing with the payment and delivery systems
        else:
            # TODO
            pass"""


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
