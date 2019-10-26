from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Topping, Order, ToppingOrderItem, FoodOrderItem
from .helpers.orderUtils import OrderState, getCurrentOrderForUser, getTotalOrderPrice, getAllOrderDetails, \
    getAllFoodContextDict, getUserDependentContextDict
from .helpers.PizzaOrderHandler import PizzaOrderHandler
from .helpers.WebpageRenderer import getAllOnePriceFoodCategoriesWithFood, getAllTwoPriceFoodCategoriesWithFood

pizzaOrderHandler = PizzaOrderHandler()

allOnePriceFood = getAllOnePriceFoodCategoriesWithFood()
allTwoPriceFood = getAllTwoPriceFoodCategoriesWithFood()


def index(request):
    message = {
        "specPizza": "Special Pizza: tomato base, grilled broccoli, courgette, sweetcorn, tomato, cashew 'mozzarella'!"
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

    if request.user.is_authenticated:
        order = getCurrentOrderForUser(request.user)

        context.update(getUserDependentContextDict(order, pizzaOrderHandler))

    return render(request, "menu.html", context)


def add(request, category, name, price):
    context = getAllFoodContextDict()

    order = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)

    if category == "Regular pizza" or category == "Sicilian pizza":
        pizzaOrderHandler.createPizzaOrderItem(order, category, name, price)
        context["toppingInformationMessage"] = "You can choose " + str(
            pizzaOrderHandler.getRemainingToppingAllowance()) + " toppings(s)."
    elif category == "Topping":
        currentPizza = pizzaOrderHandler.getCurrentPizza()
        if currentPizza and pizzaOrderHandler.isCurrentPizzaToppable():
            pizzaOrderHandler.addTopping(category, name)
            context["toppingInformationMessage"] = "You can add " + str(
                pizzaOrderHandler.getRemainingToppingAllowance()) + " more topping(s)."
        else:
            context["toppingInformationMessage"] = "Please order an eligible pizza to put topping on."
    else:
        foodOrderItem = FoodOrderItem(order=order, category=category, name=name, price=price)
        foodOrderItem.save()

    if request.user.is_authenticated:
        context.update(getUserDependentContextDict(order, pizzaOrderHandler))

    return render(request, "menu.html", context)


def deleteItemFromCart(request, category, name, price):
    context = getAllFoodContextDict()

    order = getCurrentOrderForUser(request.user)

    if category == "Topping":
        toppingToRemove = ToppingOrderItem.objects.filter(category=category, name=name).last()
        toppingToRemove.delete()
        pizzaOrderHandler.increaseToppingAllowance()
        context["toppingInformationMessage"] = "You can add " + str(
            pizzaOrderHandler.getRemainingToppingAllowance()) + " more topping(s)."
    else:
        itemToRemove = FoodOrderItem.objects.filter(order=order, category=category, name=name, price=price).last()
        itemToRemove.delete()

    context.update(getUserDependentContextDict(order, pizzaOrderHandler))

    return render(request, "menu.html", context)


def checkoutOrder(request):
    userOrder = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)
    pizzasToOrder = pizzaOrderHandler.getAllPizzasToToppingsInOrder(userOrder)

    context = {
        "user": request.user,
        "order": FoodOrderItem.objects.filter(order=userOrder),
        "total": getTotalOrderPrice(userOrder),
        "pizzasToOrder": pizzasToOrder
    }

    return render(request, "checkout.html", context)


def confirmOrder(request):
    userOrder = Order.objects.get(user=request.user, status=OrderState.INITIATED.value)
    userOrder.status = OrderState.CONFIRMED.value
    userOrder.save()

    return render(request, "index.html", {"message": "Thank you, your order has been placed!"})


def manageConfirmedOrdersAdmin(request):
    allOrders = Order.objects.filter(status=OrderState.CONFIRMED.value)

    allOrderDetailsList = getAllOrderDetails(allOrders)

    context = {
        "allOrderDetailsList": allOrderDetailsList
    }

    return render(request, "manageConfirmedOrdersAdmin.html", context)


def completeOrderAdmin(request, orderNumber):
    order = Order.objects.get(orderNumber=int(orderNumber))
    order.status = OrderState.COMPLETED.value
    order.save()

    return manageConfirmedOrdersAdmin(request)


def markOrderDeliveredAdmin(request):
    userOrder = Order.objects.get(user=request.user, status=OrderState.COMPLETED.value)
    userOrder.status = OrderState.DELIVERED.value
    userOrder.save()

    return manageConfirmedOrdersAdmin(request)


def displayUserOwnOrders(request):
    userPendingOrders = Order.objects.filter(user=request.user, status=OrderState.CONFIRMED.value)
    pendingOrderDetailsList = getAllOrderDetails(userPendingOrders)

    userCompletedOrders = Order.objects.filter(user=request.user, status=OrderState.COMPLETED.value)
    completedOrderDetailsList = getAllOrderDetails(userCompletedOrders)

    context = {
        "pendingOrders": pendingOrderDetailsList,
        "completedOrders": completedOrderDetailsList
    }

    return render(request, "userOwnOrders.html", context)
