from rest_framework import serializers

from .constants import DETAILS_LABEL, ID_LABEL, NAME_LABEL
from .models import Order, Product


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context["request"].query_params.get("fields")
        if fields:
            fields = fields.split(",")
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ProductSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Product
        fields = [ID_LABEL, NAME_LABEL, DETAILS_LABEL]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "user",
            "status",
            "delivery_datetime",
        ]  # TODO the frontend would probably need the order items too
