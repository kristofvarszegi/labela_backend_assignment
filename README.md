# Initial remarks

* No user management implemented yet due to time constraints. Features can be tried and tested using the test user ID 2.

# Set-Up and Demo Guide

1. docker-compose up -d --build
2. (Optional) Run the feature tests: ```docker-compose exec web python manage.py test```
3. Create a Django superuser (will get user ID 1): ```docker-compose exec web python manage.py createuser```
4. On the Django admin page create a simple user (will have the id 2)
5. Start the app: ```docker-compose exec web python manage.py runserver 127.0.0.1:8001```
6. Add products one by one like: ```curl -XPOST "http://127.0.0.1:8000/products/" -H "Content-Type: application/json" -d '{"name": "Lexani Rim Set", "details": "The beautiful Lexani Rim set"}'```
7. (Optional) Check the products you added: ```curl -XGET "http://127.0.0.1:8000/products/"```
8. Add products to the cart like: ```curl -XPOST "http://127.0.0.1:8000/cart/2/" -H "Content-Type: application/json" -d '{"product_id": 2}'```
9. Check the cart contents: ```curl -XGET "http://127.0.0.1:8000/cart/2/"```
10. TODO

## Useful commands

```docker exec -it labela_backend_assignment-db-1 psql -U postgres```

# Acceptance checklist

| User Story | Status | Comment |
| --- | --- | --- |
| All my products in a database | DONE | Migrate using Django to have the tables in the db. Add products on the Django admin page.
| Add a product to my shopping cart | DONE | |
| Remove a product from my shopping cart | DONE | |
| Order the current contents in my shopping cart | DONE | |
| Select a delivery date and time | DONE | |
| See an overview of all the products | DONE | |
| View the details of a product | DONE | |
| Use Postgres w/ Docker | DONE | |
| Create a RESTful API | TODO | |
| Use an ORM | DONE | Django ORM |
| Write setup doc | TODO | |

# Future next steps

* See TODOs in the code
* 1 cart per user instead of the current single global cart
* User authentication & authorizations
* Time zone support