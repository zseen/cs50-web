from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import RegularPizza, SicilianPizza, Topping, Pasta, DinnerPlatter, Salad, Sub, OrderItem, Food, OnePriceFood, \
    Order, OrderCounter

INITIATED = 'Sizzling in the kitchen'


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
        assignOrderNumberToUser(user)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html", {"message": "Please provide a unique username and email."})


def assignOrderNumberToUser(user):
    orderCounter = OrderCounter.objects.first()
    orderNumber = Order(user=user, orderNumber=orderCounter.counter)
    orderNumber.save()
    orderCounter.counter += 1
    orderCounter.save()


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
            "regularPizzas": RegularPizza.objects.all()}

    if request.user.is_authenticated:
        context["user"] = request.user
        context["order"] = OrderItem.objects.filter(user=request.user, status=INITIATED) ####???????

    return render(request, "menu.html", context)


def add(request, category, name, price):
    context = {
        "pastas": Pasta.objects.all(),
        "regularPizzas": RegularPizza.objects.all()}

    orderNumber = Order.objects.get(user=request.user, status=INITIATED).orderNumber
    orderItem = OrderItem(user=request.user, number=orderNumber, category=category, name=name, price=price)
    orderItem.save()

    if request.user.is_authenticated:
        context["user"] = request.user
        context["order"] = Order.objects.filter(user=request.user, status=INITIATED) ###????????

    return render(request, "menu.html", context)
