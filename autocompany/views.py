import json
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from autocompany.models import ORDER_STATUS_IN_CART, Order, Product
from autocompany.serializers import ProductSerializer


PRODUCT_ID_LABEL = "product_id"


@api_view(["POST"])
def add_product_to_cart(request):
    # FIXME Write serializer for Product
    product_id = json.loads(request.body)[PRODUCT_ID_LABEL]
    customer_id = 2  # TODO 1 cart per user instead of the current single global cart
    shopping_carts = Order.objects.filter(
        user_id=customer_id, status=ORDER_STATUS_IN_CART
    )
    shopping_cart_count = len(shopping_carts)
    assert shopping_cart_count < 2
    if shopping_cart_count == 1:
        shopping_cart = shopping_carts[0]
    else:
        user = User.objects.get(pk=customer_id)
        shopping_cart = Order.objects.create(
            user=user, status=ORDER_STATUS_IN_CART
        ).get()
    # product = TODO
    if shopping_cart.has_product(product_id):
        return Response("Aready in cart", status=status.HTTP_400_BAD_REQUEST)
    else:
        shopping_cart.add_product(product_id)
        return Response("Added", status.HTTP_200_OK)


"""def remove_product_from_cart(request):
    try:
        customer_id = 0  # TODO
        shopping_carts = Order.objects.filter(
            customer_id__eq=customer_id, status__eq=ORDER_STATUS_IN_CART
        )
        assert len(shopping_carts) == 1
        shopping_cart = shopping_carts[0]
        # product = TODO
        if shopping_cart.has_product(product):
            shopping_cart.remove_product(product)
            return HttpResponse("Removed")  # TODO HTTP code
        else:
            return HttpResponse("Not in cart")  # TODO HTTP code
    except Exception as e:
        return_default_error(e)


def set_delivery_datetime(request):
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
