from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import RegularPizza, SicilianPizza, Topping, Pasta, DinnerPlatter, Salad, Sub, Order, Food, OnePriceFood, \
    UserOrder, OrderCounter


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

    orderCounter = OrderCounter.objects.first()
    orderNumber = UserOrder(user=user, orderNumber=orderCounter.counter)
    orderNumber.save()
    orderCounter.counter += 1
    orderCounter.save()

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
    if not request.user.is_authenticated:
        context = {
            "pastas": Pasta.objects.all(),
            "regularPizzas": RegularPizza.objects.all()
        }
        return render(request, "menu.html", context)

    if not UserOrder.objects.get(user=request.user, status='Sizzling in the kitchen').orderNumber:
        userOrder = UserOrder(user=request.user, status='Sizzling in the kitchen', orderNumber=0)
        userOrder.save()
        orderNumber = 0
    else:
        orderNumber = UserOrder.objects.get(user=request.user, status='Sizzling in the kitchen').orderNumber

    context = {
        "user": request.user,
        "pastas": Pasta.objects.all(),
        "regularPizzas": RegularPizza.objects.all(),
        "order": Order.objects.filter(user=request.user, number=orderNumber),
    }
    return render(request, "menu.html", context)


def add(request, category, name, price):
    if not request.user.is_authenticated:
        context = {
            "pastas": Pasta.objects.all(),
            "regularPizzas": RegularPizza.objects.all()
        }
        return render(request, "menu.html", context)

    orderNumber = UserOrder.objects.get(user=request.user, status='Sizzling in the kitchen').orderNumber
    order = Order(user=request.user, number=orderNumber, category=category, name=name, price=price)
    order.save()

    context = {
        "user": request.user,
        "pastas": Pasta.objects.all(),
        "regularPizzas": RegularPizza.objects.all(),
        "order": Order.objects.filter(user=request.user, number=orderNumber)
    }
    return render(request, "menu.html", context)
