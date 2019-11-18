from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu", views.menu, name="menu"),
    path("add/<str:category>/<str:name>", views.add, name="add"),
    path("add/<str:category>/<str:name>/<str:price>", views.add, name="add"),
    path("deleteItemFromCart/<str:category>/<str:name>", views.deleteItemFromCart, name="deleteItemFromCart"),
    path("deleteItemFromCart/<str:category>/<str:name>/<str:price>", views.deleteItemFromCart, name="deleteItemFromCart"),
    path("checkoutOrder", views.checkoutOrder, name="checkoutOrder"),
    path("confirmOrder", views.confirmOrder, name="confirmOrder"),
    path("manageConfirmedOrdersAdmin", views.manageConfirmedOrdersAdmin, name="manageConfirmedOrdersAdmin"),
    path("completeOrderAdmin/<str:orderNumber>", views.completeOrderAdmin, name="completeOrderAdmin"),
    path("markOrderDeliveredAdmin/<str:orderNumber>", views.markOrderDeliveredAdmin, name="markOrderDeliveredAdmin"),
    path("displayUserOwnOrders", views.displayUserOwnOrders, name="displayUserOwnOrders")
]
