import json
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ID_LABEL, ORDER_STATUS_IN_CART, Order, OrderItem, Product
from .serializers import ProductSerializer


DELIVERY_DATETIME_LABEL = "delivery_datetime"
ITEMS_LABEL = "items"
ORDER_ID_LABEL = "order_id"
PRODUCT_ID_LABEL = "product_id"
STATUS_LABEL = "status"
USER_ID_LABEL = "user_id"

TEST_USER_ID = (
    2  # TODO 1 cart per user instead of the current single global user and cart
)


class CartManager(APIView):
    def get(self, request, user_id):
        order_query = Order.objects.filter(user_id=user_id)
        if order_query.exists():
            order = order_query.get()
            order_items = list(OrderItem.objects.filter(order_id=order.id))
            # TODO find the way to use the serializer for this
            order_item_dicts = list()
            for order_item in order_items:
                order_item_dicts.append(
                    {
                        ID_LABEL: order_item.id,
                        ORDER_ID_LABEL: order_item.order_id,
                        PRODUCT_ID_LABEL: order_item.product_id,
                    }
                )
            order_dict = {
                ID_LABEL: order.id,
                USER_ID_LABEL: order.user_id,
                STATUS_LABEL: order.status,
                DELIVERY_DATETIME_LABEL: order.delivery_datetime,
                ITEMS_LABEL: order_item_dicts,
            }
            return Response(order_dict, status.HTTP_200_OK)
        else:
            return Response(f"Cart of user {user_id} is empty", status.HTTP_200_OK)

    def post(self, request, user_id):
        # TODO Write serializer for Product
        product_id = json.loads(request.body)[PRODUCT_ID_LABEL]
        shopping_carts = Order.objects.filter(
            user_id=user_id, status=ORDER_STATUS_IN_CART
        )
        shopping_cart_count = len(shopping_carts)
        assert shopping_cart_count < 2
        if shopping_cart_count == 1:
            shopping_cart = shopping_carts[0]
        else:
            user = User.objects.get(pk=user_id)
            shopping_cart = Order.objects.create(user=user, status=ORDER_STATUS_IN_CART)
        if shopping_cart.has_product(product_id):
            return Response("Aready in cart", status=status.HTTP_400_BAD_REQUEST)
        else:
            shopping_cart.add_product(product_id)
            return Response("Added", status.HTTP_200_OK)

    def delete(self, request, user_id):
        product_id = json.loads(request.body)[PRODUCT_ID_LABEL]
        shopping_carts = Order.objects.filter(
            user_id=user_id, status=ORDER_STATUS_IN_CART
        )
        shopping_cart_count = len(shopping_carts)
        assert shopping_cart_count < 2
        if shopping_cart_count == 1:
            shopping_cart = shopping_carts[0]
            if shopping_cart.has_product(product_id):
                OrderItem.objects.filter(
                    order_id=shopping_cart.id, product_id=product_id
                ).delete()
                return Response("Deleted", status.HTTP_200_OK)
            else:
                return Response(
                    "Product {product_id} is not in cart of user {user_id}",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                f"Cart of user {user_id} is empty", status=status.HTTP_400_BAD_REQUEST
            )


"""def set_delivery_datetime(request):
    try:
        # delivery_datetime = TODO
        shopping_carts = Order.objects.filter(
            customer_id__eq=customer_id, status__eq=ORDER_STATUS_IN_CART
        )
        shopping_cart_count = len(shopping_carts)
        if shopping_cart_count > 1:
            # TODO
            pass
        elif shopping_cart_count == 0:
            # TODO
            pass
        else:
            shopping_cart = shopping_carts[0]
            if shopping_cart.is_delivery_datetime_valid():
                shopping_cart.set_delivery_datetime(delivery_datetime)
            else:
                # TODO
                pass
    except Exception as e:
        return_default_error(e)


def submit_order(request):
    try:
        orders = Order.objects.filter(id__eq=order_id)
        assert len(orders) == 1
        order = orders[0]
        if order.is_delivery_datetime_valid():
            order.submit()
        else:
            # TODO
            pass
        # TODO
        pass
    except Exception as e:
        return_default_error(e)
"""


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # TODO handle if a product with the same name already exists
