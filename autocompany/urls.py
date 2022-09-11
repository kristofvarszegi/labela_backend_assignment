"""autocompany URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from autocompany import views

urlpatterns = [
    # path("api/cart/product/add", views.add_product_to_cart),
    # path("api/cart/product/remove", views.remove_product_from_cart),
    # path("api/cart/delivery-datetime/set", views.set_delivery_datetime),
    # path("api/cart/submit", views.submit_order),
    path("api/product/all", views.get_all_products),
    # path("api/product/<id:TODO>/details", views.get_product_details),
    path("admin/", admin.site.urls),
]
