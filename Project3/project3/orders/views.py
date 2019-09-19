from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import RegularPizza, SicilianPizza, Topping, Pasta, DinnerPlatter, Salad, Sub, OrderItem, Order
from .helpers.orderUtils import OrderState, getCurrentOrderForUser, getTotalOrderPrice, AllOrderDetails


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")

    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]

    user = User.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    if user:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html", {"message": "Please provide a unique username and email."})


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"message": "Invalid username or password."})


def logout_view(request):
    logout(request)
    return render(request, "index.html")


def menu(request):
    context = {
        "pastas": Pasta.objects.all(),
        "regularPizzas": RegularPizza.objects.all()
    }

    if request.user.is_authenticated:
        order = getCurrentOrderForUser(request.user)

        context["user"] = request.user
        context["order"] = OrderItem.objects.filter(order=order)
        context["total"] = getTotalOrderPrice(order)

    return render(request, "menu.html", context)


def add(request, category, name, price):
    context = {
        "pastas": Pasta.objects.all(),
        "regularPizzas": RegularPizza.objects.all()
    }

    order = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)

    orderItem = OrderItem(order=order, category=category, name=name, price=price)
    orderItem.save()

    if request.user.is_authenticated:
        context["user"] = request.user
        context["order"] = OrderItem.objects.filter(order=order)
        context["total"] = getTotalOrderPrice(order)

    return render(request, "menu.html", context)


def checkoutOrder(request):
    userOrder = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)
    context = {
        "user": request.user,
        "order": OrderItem.objects.filter(order=userOrder),
        "total": getTotalOrderPrice(userOrder)
    }

    return render(request, "checkout.html", context)


def confirmOrder(request):
    userOrder = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)
    userOrder.status = OrderState.CONFIRMED.value
    userOrder.save()

    return render(request, "index.html", {"message": "Thank you, your order has been placed!"})


def viewConfirmedOrders(request):
    allOrders = Order.objects.filter(status=OrderState.CONFIRMED.value)

    foodInAllOrdersFinder = AllOrderDetails()
    ordersWithOrderItems = foodInAllOrdersFinder.getOrderItemsToAllOrdersList(allOrders)

    context = {
        "ordersWithOrderItems": ordersWithOrderItems
    }

    return render(request, "orders.html", context)
