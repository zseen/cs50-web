from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import RegularPizza, SicilianPizza, Topping, Pasta, DinnerPlatter, Salad, Sub, Order2, Food, OnePriceFood



def index(request):
    if not request.user:
        return render(request, "login.html")

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
    context={
        "user": request.user,
        "pastas": Pasta.objects.all(),
        "regularPizzas": RegularPizza.objects.all(),
        "order": Order2.objects.filter(user=request.user)

    }
    return render(request, "menu.html", context)


def add(request, category, name, price):
    userOrder = Order2(user=request.user, number=1, category=category, name=name, price=price)
    userOrder.save()

    context = {
        "user": request.user,
        "pastas": Pasta.objects.all(),
        "regularPizzas": RegularPizza.objects.all(),
        "order": Order2.objects.filter(user=request.user)
    }
    return render(request, "menu.html", context)
