import json
from django.db import models
from datetime import datetime, timedelta

APP_LABEL = "autocompany"

ID_LABEL = "id"
DETAILS_LABEL = "details"
NAME_LABEL = "name"


class Product(models.Model):
    name = models.CharField(max_length=255)
    details = models.CharField(max_length=4095)

    class Meta:
        app_label = APP_LABEL


"""ORDER_STATUS_IN_CART = 0
ORDER_STATUS_SUBMITTED = 1
ORDER_STATUS_EN_ROUTE = 2
ORDER_STATUS_DELIVERED = 3


class Order(models.Model):
    # TODO use properties
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="Order"
    )
    order_items = models.ManyToOneRel(
        OrderItem, on_delete=models.CASCADE, related_name="Order"
    )
    status = models.PositiveIntegerField()
    delivery_datetime = models.DateTimeField()  # TODO

    def has_product(self, product: Product):
        return (
            len(
                filter(
                    lambda order_item: order_item.product_id == product.id,
                    OrderItems.objects.filter(order_id__eq=shopping_cart.id),
                )
            )
            > 0
        )

    def add_product(self, product: Product):
        if self.status != ORDER_STATUS_IN_CART:
            raise ValueError(
                f"Cannot add product {product} to order {self.id}: order has already been submitted."
            )  # TODO find a more exact error type for this case
        order_item = OrderItem(self, product)
        order_item.save()

    def remove_product(self, product: Product):
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
            pass


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="OrderItem")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="Product"
    )
"""
