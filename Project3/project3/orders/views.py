from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Order, FoodOrderItem, OrderItem
from .helpers.OrderUtils import OrderState, getCurrentOrderForUser, getTotalOrderPrice, getAllOrderDetails, \
    getAllFoodContextDict, getUserDependentContextDict, SPECIAL_PIZZA
from .helpers.PizzaOrderHandler import PizzaOrderHandler, PizzaCategory, TOPPING, \
    RemainingToppingAllowanceMessageGenerator

pizzaOrderHandler = PizzaOrderHandler()
messageGenerator = RemainingToppingAllowanceMessageGenerator(pizzaOrderHandler)


def index(request):
    message = {
        "specialPizza": SPECIAL_PIZZA
    }

    return render(request, "index.html", message)


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
    context = getAllFoodContextDict()

    # rows = Order.objects.filter()
    #
    # for r in rows:
    #     r.delete()
    #
    # rows = OrderItem.objects.filter()
    #
    # for r in rows:
    #     r.delete()

    if request.user.is_authenticated:
        order = getCurrentOrderForUser(request.user)
        pizzasToToppingsInOrder = pizzaOrderHandler.getAllPizzasToToppingsInUserOrder(order)
        currentPizza = pizzaOrderHandler.getCurrentPizza()
        context.update(getUserDependentContextDict(order, currentPizza, pizzasToToppingsInOrder))
        return render(request, "menuLoggedIn.html", context)

    return render(request, "menu.html", context)


def add(request, category, name, price=""):
    context = getAllFoodContextDict()

    order = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)

    if category == PizzaCategory.REGULAR_PIZZA.value or category == PizzaCategory.SICILIAN_PIZZA.value:
        pizzaOrderHandler.createPizzaOrderItem(order, category, name, price)
        context["toppingInformationMessage"] = messageGenerator.getRemainingToppingAllowanceMessage(
            order)
    elif category == TOPPING:
        pizzaOrderHandler.addTopping(category, name)
        context["toppingInformationMessage"] = messageGenerator.getRemainingToppingAllowanceMessage(
            order)
    else:
        foodOrderItem = FoodOrderItem(order=order, category=category, name=name, price=price)
        foodOrderItem.save()

    if request.user.is_authenticated:
        pizzasToToppingsInOrder = pizzaOrderHandler.getAllPizzasToToppingsInUserOrder(order)
        currentPizza = pizzaOrderHandler.getCurrentPizza()
        context.update(getUserDependentContextDict(order, currentPizza, pizzasToToppingsInOrder))
        return render(request, "menuLoggedIn.html", context)

    return render(request, "menu.html", context)


def deleteItemFromCart(request, category, name, price=""):
    context = getAllFoodContextDict()

    order = getCurrentOrderForUser(request.user)

    if category == TOPPING:
        pizzaOrderHandler.removeTopping(category, name)
        context["toppingInformationMessage"] = messageGenerator.getRemainingToppingAllowanceMessage(
            order)
    else:
        itemToRemove = FoodOrderItem.objects.filter(order=order, category=category, name=name, price=price).last()
        itemToRemove.delete()

    currentPizza = pizzaOrderHandler.getCurrentPizza()
    pizzasToToppingsInOrder = pizzaOrderHandler.getAllPizzasToToppingsInUserOrder(order)
    context.update(getUserDependentContextDict(order, currentPizza, pizzasToToppingsInOrder))

    return render(request, "menuLoggedIn.html", context)


def checkoutOrder(request):
    userOrder = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)
    pizzasWithToppingsInOrder = pizzaOrderHandler.getAllPizzasToToppingsInUserOrder(userOrder)

    context = {
        "order": FoodOrderItem.objects.filter(order=userOrder),
        "total": getTotalOrderPrice(userOrder),
        "pizzasWithToppingsInOrder": pizzasWithToppingsInOrder
    }

    return render(request, "checkout.html", context)


def confirmOrder(request):
    userOrder = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)
    userOrder.status = OrderState.CONFIRMED.value
    userOrder.save()

    return render(request, "index.html", {"message": "Thank you, your order has been placed!"})


def manageConfirmedOrdersAdmin(request):
    allConfirmedOrders = Order.objects.filter(status=OrderState.CONFIRMED.value)
    allCompletedOrders = Order.objects.filter(status=OrderState.COMPLETED.value)

    allConfirmedOrderDetailsList = getAllOrderDetails(allConfirmedOrders)
    allCompletedOrderDetailsList = getAllOrderDetails(allCompletedOrders)

    context = {
        "allConfirmedOrderDetailsList": allConfirmedOrderDetailsList,
        "allCompletedOrderDetailsList": allCompletedOrderDetailsList
    }

    return render(request, "manageConfirmedOrdersAdmin.html", context)


def completeOrderAdmin(request, orderNumber):
    order = Order.objects.get(orderNumber=int(orderNumber))
    order.status = OrderState.COMPLETED.value
    order.save()

    return manageConfirmedOrdersAdmin(request)


def markOrderDeliveredAdmin(request, orderNumber):
    userOrder = Order.objects.get(orderNumber=int(orderNumber))
    userOrder.status = OrderState.DELIVERED.value
    userOrder.save()

    return manageConfirmedOrdersAdmin(request)


def displayUserOwnOrders(request):
    userPendingOrConfirmedOrders = Order.objects.filter(status=OrderState.CONFIRMED.value) | Order.objects.filter(
        status=OrderState.COMPLETED.value)
    pendingOrCompletedOrderDetailsListt = getAllOrderDetails(userPendingOrConfirmedOrders)

    userDeliveredOrders = Order.objects.filter(user=request.user, status=OrderState.DELIVERED.value)
    deliveredOrderDetailsList = getAllOrderDetails(userDeliveredOrders)

    context = {
        "pendingOrConfirmedOrders": pendingOrCompletedOrderDetailsListt,
        "deliveredOrders": deliveredOrderDetailsList
    }

    return render(request, "userOwnOrders.html", context)
