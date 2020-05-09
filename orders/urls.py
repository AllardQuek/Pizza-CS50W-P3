from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("cart", views.cart, name="cart"),
    path("add", views.add_to_cart, name="addtocart"),
    path("addsub", views.add_sub, name="addsub"),
    path("addpasta", views.add_pasta, name="addpasta"),
    path("addsalad", views.add_salad, name="addsalad"),
    path("addplatter", views.add_platter, name="addplatter"),
    path("order", views.order, name="order"),
    path("vieworders", views.view_orders, name="vieworders"),
]
