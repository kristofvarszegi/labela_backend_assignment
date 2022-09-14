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
from django.urls import include, path
from rest_framework import routers

from autocompany import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("cart/<int:user_id>/", views.CartManager.as_view()),
    path(
        "cart/<int:user_id>/delivery-datetime/",
        views.set_delivery_datetime,
    ),
    path("cart/<int:user_id>/submit/", views.submit),
]
# TODO define urls by referencing views instead of hardcoding
