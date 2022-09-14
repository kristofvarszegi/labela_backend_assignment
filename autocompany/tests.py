import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from .models import OrderItem, Product, DETAILS_LABEL, ID_LABEL, NAME_LABEL
from .views import (
    ITEMS_LABEL,
    ORDER_ID_LABEL,
    PRODUCT_ID_LABEL,
    TEST_USER_ID,
    USER_ID_LABEL,
)


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
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_and_assert_cart(self, user_id, product_ids: list):
        response = self.client.get(f"/cart/{user_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = json.loads(response.content)
        self.assertEqual(cart[USER_ID_LABEL], user_id)
        self.assertEqual(len(cart[ITEMS_LABEL]), len(product_ids))
        for i, order_item in enumerate(cart[ITEMS_LABEL]):
            self.assertEqual(order_item[ORDER_ID_LABEL], cart[ID_LABEL])
            self.assertEqual(order_item[PRODUCT_ID_LABEL], product_ids[i])

    def test_list_products(self):
        prepopulated_products = list(Product.objects.all())
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products_downloaded = json.loads(response.content)
        self.assertEqual(len(products_downloaded), len(prepopulated_products))
        for i, prepopulated_product in enumerate(prepopulated_products):
            self.assertIn(ID_LABEL, products_downloaded[i])
            self.assertEqual(
                products_downloaded[i][NAME_LABEL], prepopulated_product.name
            )
            self.assertEqual(
                products_downloaded[i][DETAILS_LABEL], prepopulated_product.details
            )

    def test_list_product_names(self):
        prepopulated_products = list(Product.objects.all())
        response = self.client.get("/products/?fields=id,name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        downloaded_products = json.loads(response.content)
        self.assertEqual(len(downloaded_products), len(prepopulated_products))
        for i, prepopulated_product in enumerate(prepopulated_products):
            self.assertEqual(len(downloaded_products[i].keys()), 2)  # id, name
            self.assertIn(ID_LABEL, downloaded_products[i])
            self.assertEqual(
                downloaded_products[i][NAME_LABEL], prepopulated_product.name
            )

    def test_retrieve_product_details(self):
        prepopulated_products = list(Product.objects.all())
        prepopulated_product = prepopulated_products[0]
        response = self.client.get(
            f"/products/{prepopulated_product.id}/?fields=id,details"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_product = json.loads(response.content)
        self.assertEqual(len(retrieved_product.keys()), 2)  # id, name
        self.assertIn(ID_LABEL, retrieved_product)
        self.assertEqual(retrieved_product[ID_LABEL], prepopulated_product.id)
        self.assertEqual(retrieved_product[DETAILS_LABEL], prepopulated_product.details)

    def test_add_product_to_cart(self):
        user_id = TEST_USER_ID

        product_ids = [2]
        self.add_products_to_cart(user_id, product_ids)

        self.get_and_assert_cart(user_id, product_ids)

    def test_remove_product_from_cart(self):
        user_id = TEST_USER_ID

        product_ids_to_add = [2, 3]
        self.add_products_to_cart(user_id, product_ids_to_add)

        product_id_to_remove = 2
        response = self.client.delete(
            f"/cart/{user_id}/",
            content_type="application/json",
            data={PRODUCT_ID_LABEL: product_id_to_remove},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        remaining_product_ids = [
            product_id
            for product_id in product_ids_to_add
            if product_id != product_id_to_remove
        ]
        self.get_and_assert_cart(user_id, remaining_product_ids)
