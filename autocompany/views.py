import json
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import (
    DATETIME_FORMAT,
    DELIVERY_DATETIME_LABEL,
    ID_LABEL,
    ITEMS_LABEL,
    ORDER_ID_LABEL,
    ORDER_STATUS_IN_CART,
    PRODUCT_ID_LABEL,
    STATUS_LABEL,
    TEST_USER_ID,
    USER_ID_LABEL,
)
from .models import Order, OrderItem, Product
from .serializers import ProductSerializer


# TODO check user id validity
class CartManager(APIView):
    @staticmethod
    def get_cart(user_id: int):
        carts = Order.objects.filter(user_id=user_id, status=ORDER_STATUS_IN_CART)
        cart_count = len(carts)
        assert cart_count < 2
        if cart_count == 1:
            return carts[0]
        else:
            return None

    @staticmethod
    def create_resonse_request_body_invalid():
        return Response("Request body invalid", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create_response_request_body_missing(missing_field):
        return Response(
            f"Request body missing {missing_field}",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def create_response_cart_is_empty(user_id, http_status=status.HTTP_400_BAD_REQUEST):
        return Response(f"Cart of user {user_id} is empty", status=http_status)

    def get(self, _, user_id):
        # TODO resolve after user authentication added
        if user_id != TEST_USER_ID:
            return Response(
                "User ID must be 2 at the current development stage",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (cart := CartManager.get_cart(user_id)) is None:
            return CartManager.create_response_cart_is_empty(
                user_id, status.HTTP_204_NO_CONTENT
            )
        items = list(OrderItem.objects.filter(order_id=cart.id))
        # TODO find the way to use the serializer for this
        item_dicts = list()
        for item in items:
            item_dicts.append(
                {
                    ID_LABEL: item.id,
                    ORDER_ID_LABEL: item.order_id,
                    PRODUCT_ID_LABEL: item.product_id,
                }
            )
        cart_dict = {
            ID_LABEL: cart.id,
            USER_ID_LABEL: cart.user_id,
            STATUS_LABEL: cart.status,
            DELIVERY_DATETIME_LABEL: cart.delivery_datetime,
            ITEMS_LABEL: item_dicts,
        }
        return Response(cart_dict, status.HTTP_200_OK)

    def post(self, request, user_id):
        try:
            request_body_json = json.loads(request.body)
            if PRODUCT_ID_LABEL in request_body_json:
                product_id = request_body_json[PRODUCT_ID_LABEL]
            else:
                return CartManager.create_response_request_body_missing(
                    PRODUCT_ID_LABEL
                )
        except ValueError:
            return CartManager.create_resonse_request_body_invalid()
        if (cart := CartManager.get_cart(user_id)) is None:
            user = User.objects.get(pk=user_id)
            cart = Order.objects.create(user=user, status=ORDER_STATUS_IN_CART)
        if cart.has_product(product_id):
            return Response("Already in cart", status=status.HTTP_400_BAD_REQUEST)
        else:
            cart.add_product(product_id)
            return Response("Added", status.HTTP_200_OK)

    def delete(self, request, user_id):
        try:
            request_body_json = json.loads(request.body)
            if PRODUCT_ID_LABEL in request_body_json:
                product_id = request_body_json[PRODUCT_ID_LABEL]
            else:
                return CartManager.create_response_request_body_missing(
                    PRODUCT_ID_LABEL
                )
        except ValueError:
            return CartManager.create_resonse_request_body_invalid()
        if (cart := CartManager.get_cart(user_id)) is None:
            return CartManager.create_response_cart_is_empty(user_id)
        try:
            cart.remove_product(product_id)
            return Response("Item deleted from cart", status.HTTP_200_OK)
        except ValueError as ve:
            return Response(ve, status=status.HTTP_400_BAD_REQUEST)


# TODO figure out why these don't work if inside the class and registering with as_view(<kwargs>)
@api_view(["POST"])
def set_delivery_datetime(request, user_id):
    try:
        request_body_json = json.loads(request.body)
        if DELIVERY_DATETIME_LABEL in request_body_json:
            delivery_datetime = request_body_json[DELIVERY_DATETIME_LABEL]
        else:
            return CartManager.create_response_request_body_missing(
                DELIVERY_DATETIME_LABEL
            )
    except ValueError:
        return CartManager.create_resonse_request_body_invalid()
    try:
        delivery_datetime = datetime.strptime(delivery_datetime, DATETIME_FORMAT)
    except ValueError:
        return Response(
            "Invalid delivery datetime",
            status=status.HTTP_400_BAD_REQUEST,
        )
    if Order.is_delivery_datetime_valid(delivery_datetime):
        if (cart := CartManager.get_cart(user_id)) is None:
            return CartManager.create_response_cart_is_empty(user_id)
        cart.set_delivery_datetime(delivery_datetime)
        return Response(data={ID_LABEL: cart.id}, status=status.HTTP_200_OK)
    else:
        return Response("Invalid delivery datetime", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def submit(_, user_id):
    if (cart := CartManager.get_cart(user_id)) is None:
        return CartManager.create_response_cart_is_empty(user_id)
    if Order.is_delivery_datetime_valid(cart.delivery_datetime):
        cart.submit()
        return Response(data={ID_LABEL: cart.id}, status=status.HTTP_200_OK)
    else:
        return Response(
            f"Cart of user {user_id} has no delivery datetime",
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # TODO handle if a product with the same name already exists
