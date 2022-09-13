import json
from django.test import TestCase
from rest_framework import status

from autocompany.models import ID_LABEL, NAME_LABEL, DETAILS_LABEL
from autocompany.views import PRODUCT_ID_LABEL


# TODO assert response HTTP status codes too
class ProductApiTest(TestCase):
    @staticmethod
    def create_dummy_product_objects():
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
        return products

    def upload_dummy_products(self):
        products_to_upload = ProductApiTest.create_dummy_product_objects()
        for product in products_to_upload:
            self.client.post("/products/", data=product)
        return products_to_upload

    def test_list_products(self):
        products_to_upload = self.upload_dummy_products()
        response = self.client.get("/products/")
        products_downloaded = json.loads(response.content)
        self.assertEqual(len(products_downloaded), len(products_to_upload))
        for i, product_to_upload in enumerate(products_to_upload):
            self.assertIn(ID_LABEL, products_downloaded[i])
            for key in [DETAILS_LABEL, NAME_LABEL]:
                self.assertEqual(products_downloaded[i][key], product_to_upload[key])

    def test_list_product_names(self):
        products_to_upload = self.upload_dummy_products()
        response = self.client.get("/products/?fields=id,name")
        products_downloaded = json.loads(response.content)
        self.assertEqual(len(products_downloaded), len(products_to_upload))
        for i, product_to_upload in enumerate(products_to_upload):
            self.assertEqual(len(products_downloaded[i].keys()), 2)  # id, name
            self.assertIn(ID_LABEL, products_downloaded[i])
            self.assertEqual(
                products_downloaded[i][NAME_LABEL], product_to_upload[NAME_LABEL]
            )

    def test_retrieve_product_details(self):
        products_to_upload = ProductApiTest.create_dummy_product_objects()
        products_uploaded = list()
        for product in products_to_upload:
            response = self.client.post("/products/", data=product)
            products_uploaded.append(json.loads(response.content))
        self.assertEqual(len(products_uploaded), len(products_to_upload))
        test_product_uploaded = products_uploaded[0]
        response = self.client.get(
            f"/products/{test_product_uploaded[ID_LABEL]}/?fields=id,details"
        )
        product_detail_downloaded = json.loads(response.content)
        self.assertEqual(len(product_detail_downloaded.keys()), 2)  # id, name
        self.assertIn(ID_LABEL, product_detail_downloaded)
        for key in [ID_LABEL, DETAILS_LABEL]:
            self.assertEqual(product_detail_downloaded[key], test_product_uploaded[key])

    def test_add_product_to_cart(self):
        self.upload_dummy_products()
        product = {PRODUCT_ID_LABEL: 2}
        response = self.client.post("/orders/", data=product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO Finish
