DELIVERY_DATETIME_LABEL = "delivery_datetime"
DETAILS_LABEL = "details"
ID_LABEL = "id"
ITEMS_LABEL = "items"
NAME_LABEL = "name"
ORDER_ID_LABEL = "order_id"
PRODUCT_ID_LABEL = "product_id"
STATUS_LABEL = "status"
USER_ID_LABEL = "user_id"

TEST_USER_ID = (
    2  # TODO 1 cart per user instead of the current single global user and cart
)

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"  # TODO find a standard library function for this

ORDER_STATUS_IN_CART = 0
ORDER_STATUS_SUBMITTED = 1
ORDER_STATUS_EN_ROUTE = 2
ORDER_STATUS_DELIVERED = 3
