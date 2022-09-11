import json
from django.http import HttpResponseServerError, JsonResponse
from autocompany.models import Product  # ORDER_STATUS_IN_CART, Order, OrderItem


def return_default_error(e: Exception):
    return HttpResponseServerError(
        f"Error: {e}"
    )  # TODO proper error categorization and messaging; HTTP code


"""def add_product_to_cart(request):
    print(request.body)
    try:
        customer_id = 0  # TODO
        shopping_carts = Order.objects.filter(
            customer_id__eq=customer_id, status__eq=ORDER_STATUS_IN_CART
        )
        shopping_cart_count = len(shopping_carts)
        assert shopping_cart_count < 2
        if shopping_cart_count == 1:
            shopping_cart = shopping_carts[0]
        else:
            shopping_cart = Order(customer_id)  # TODO implement/needed?
        # product = TODO
        if shopping_cart.has_product(product):
            return HttpResponse("Aready in cart")  # TODO HTTP code
        else:
            shopping_cart.add_product(product)
            return HttpResponse("Added")  # TODO HTTP code
    except Exception as e:
        return_default_error(e)


def remove_product_from_cart(request):
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


def get_all_products(request):
    try:
        products = Product.objects.all()
        serialized_products = [
            {"name": product.name, "details": product.details} for product in products
        ]
        return JsonResponse({"products": serialized_products})
    except Exception as e:
        return_default_error(e)


"""def get_product_details(request):
    try:
        # TODO
        pass
    except Exception as e:
        return_default_error(e)
"""
