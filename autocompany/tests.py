from datetime import datetime, timedelta
import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from .constants import (
    DATETIME_FORMAT,
    DELIVERY_DATETIME_LABEL,
    DETAILS_LABEL,
    ID_LABEL,
    NAME_LABEL,
    ORDER_STATUS_SUBMITTED,
    PRODUCT_ID_LABEL,
    TEST_USER_ID,
)
from .models import Order, OrderItem, Product
from .views import CartManager


class ProductApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ProductApiTest, cls).setUpClass()
        cls.setUp_users()
        cls.setUp_products()

    @classmethod
    def setUp_users(self):
        User.objects.create(username="user1", password="user1234")
        User.objects.create(username="user2", password="user1234")
        User.objects.create(username="user3", password="user1234")

    @classmethod
    def setUp_products(self):
        # TODO load from separate JSON file
        products = list()
        products.append(
            {
                NAME_LABEL: "Lexani Rim Set",
                DETAILS_LABEL: "The beautiful Lexani Rim set",
            }
        )
        products.append(
            {
                NAME_LABEL: "Brembo Brake Set",
                DETAILS_LABEL: "The strong brembo brake set",
            }
        )
        products.append(
            {
                NAME_LABEL: "Sparco Driver's Seat",
                DETAILS_LABEL: "The comfortable Sparco driver's seat",
            }
        )
        for product in products:
            Product.objects.create(name=product["name"], details=product["details"])

    def add_products_to_cart(self, user_id: int, product_ids: list):
        for product_id in product_ids:
            response = self.client.post(
                f"/cart/{user_id}/",
                content_type="application/json",
                data={PRODUCT_ID_LABEL: product_id},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def assert_cart(self, user_id, product_ids: list):
        cart = CartManager.get_cart(user_id)
        if product_ids:
            self.assertEqual(cart.user.id, user_id)
            items = OrderItem.objects.filter(order_id=cart.id)
            self.assertEqual(len(items), len(product_ids))
            for i, item in enumerate(items):
                self.assertEqual(item.order_id, cart.id)
                self.assertEqual(item.product_id, product_ids[i])
        else:
            self.assertIsNone(cart)

    def test_list_products(self):
        prepopulated_products = list(Product.objects.all())
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        listed_products = json.loads(response.content)
        self.assertEqual(len(listed_products), len(prepopulated_products))
        for i, prepopulated_product in enumerate(prepopulated_products):
            self.assertIn(ID_LABEL, listed_products[i])
            self.assertEqual(listed_products[i][NAME_LABEL], prepopulated_product.name)
            self.assertEqual(
                listed_products[i][DETAILS_LABEL], prepopulated_product.details
            )

    def test_list_product_names(self):
        prepopulated_products = list(Product.objects.all())
        response = self.client.get("/products/?fields=id,name")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        listed_products = json.loads(response.content)
        self.assertEqual(len(listed_products), len(prepopulated_products))
        for i, prepopulated_product in enumerate(prepopulated_products):
            self.assertEqual(len(listed_products[i].keys()), 2)  # id, name
            self.assertIn(ID_LABEL, listed_products[i])
            self.assertEqual(listed_products[i][NAME_LABEL], prepopulated_product.name)

    def test_retrieve_product_details(self):
        prepopulated_products = list(Product.objects.all())
        prepopulated_product = prepopulated_products[0]
        response = self.client.get(
            f"/products/{prepopulated_product.id}/?fields=id,details"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        retrieved_product = json.loads(response.content)
        self.assertEqual(len(retrieved_product.keys()), 2)  # id, name
        self.assertIn(ID_LABEL, retrieved_product)
        self.assertEqual(retrieved_product[ID_LABEL], prepopulated_product.id)
        self.assertEqual(retrieved_product[DETAILS_LABEL], prepopulated_product.details)

    def test_add_product_to_cart(self):
        user_id = TEST_USER_ID
        product_ids = [2]
        self.add_products_to_cart(user_id, product_ids)
        self.assert_cart(user_id, product_ids)

    def test_remove_product_from_2item_cart(self):
        user_id = TEST_USER_ID
        product_ids_to_add = [2, 3]
        self.add_products_to_cart(user_id, product_ids_to_add)
        product_id_to_remove = 2
        response = self.client.delete(
            f"/cart/{user_id}/",
            content_type="application/json",
            data={PRODUCT_ID_LABEL: product_id_to_remove},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        remaining_product_ids = [
            product_id
            for product_id in product_ids_to_add
            if product_id != product_id_to_remove
        ]
        self.assert_cart(user_id, remaining_product_ids)

    def test_remove_product_from_1item_cart(self):
        user_id = TEST_USER_ID
        product_id = 3
        self.add_products_to_cart(user_id, [product_id])
        response = self.client.delete(
            f"/cart/{user_id}/",
            content_type="application/json",
            data={PRODUCT_ID_LABEL: product_id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assert_cart(user_id, [])

    def test_order_empty_cart(self):
        user_id = TEST_USER_ID
        response = self.client.post(f"/cart/{user_id}/submit/")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )
        self.assertIn("empty", response.content.decode())

        response = self.client.get(f"/cart/{user_id}/")
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )

    def test_select_cart_delivery_datetime(self):
        user_id = TEST_USER_ID

        product_ids_to_add = [2, 3]
        self.add_products_to_cart(user_id, product_ids_to_add)

        delivery_datetime = (datetime.now() + timedelta(days=10)).strftime(
            DATETIME_FORMAT
        )
        response = self.client.post(
            f"/cart/{user_id}/delivery-datetime/",
            content_type="application/json",
            data={DELIVERY_DATETIME_LABEL: delivery_datetime},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        order_id = json.loads(response.content)[ID_LABEL]
        order_query = Order.objects.filter(pk=order_id)
        self.assertTrue(order_query.exists())
        self.assertEqual(
            order_query.get().delivery_datetime.strftime(DATETIME_FORMAT),
            delivery_datetime,
        )

    def test_order_cart_contents(self):
        user_id = TEST_USER_ID

        product_ids_to_add = [2, 3]
        self.add_products_to_cart(user_id, product_ids_to_add)

        delivery_datetime = (datetime.now() + timedelta(days=10)).strftime(
            DATETIME_FORMAT
        )
        response = self.client.post(
            f"/cart/{user_id}/delivery-datetime/",
            content_type="application/json",
            data={DELIVERY_DATETIME_LABEL: delivery_datetime},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        response = self.client.post(f"/cart/{user_id}/submit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        order_id = json.loads(response.content)[ID_LABEL]
        order_query = Order.objects.filter(pk=order_id)
        self.assertTrue(order_query.exists())
        self.assertEqual(order_query.get().status, ORDER_STATUS_SUBMITTED)
