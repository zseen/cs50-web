from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu", views.menu, name="menu"),
    path("add/<str:category>/<str:name>/<str:price>", views.add, name="add"),
    path("checkoutOrder", views.checkoutOrder, name="checkoutOrder"),
    path("confirmOrder", views.confirmOrder, name="confirmOrder"),
    path("manageOrders", views.manageOrders, name="manageOrders")

]
