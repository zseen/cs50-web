from django.db.models import Sum
from orders.models import Order, OrderItem, OrderCounter, ToppingOrderItem, Topping, FoodOrderItem
from .OrderState import OrderState
from .FoodSection import getAllOnePriceFoodCategoriesWithFood, getAllTwoPriceFoodCategoriesWithFood

SPECIAL_PIZZA = "Special Pizza: tomato base, grilled broccoli, courgette, sweetcorn, tomato, cashew 'mozzarella'!"


def createNewOrderForUser(user):
    orderNumber = createNextOrderNumber()
    newUserOrder = Order(user=user, orderNumber=orderNumber)
    newUserOrder.save()
    return newUserOrder


def createNextOrderNumber():
    orderCounter = OrderCounter.objects.first()
    if not orderCounter:
        orderCounter = OrderCounter(counter=1)
        return orderCounter.counter

    orderCounter.counter += 1
    orderCounter.save()
    return orderCounter.counter


def getCurrentOrderForUser(user):
    try:
        order = Order.objects.get(user=user, status=OrderState.INITIATED.value)
    except Order.DoesNotExist:
        order = createNewOrderForUser(user)
    return order


def getTotalOrderPrice(order):
    return OrderItem.objects.filter(order=order).aggregate(Sum('price'))['price__sum']


class OrderDetails:
    def __init__(self, order):
        self._order = order

    def getOrderItemsInOrder(self):
        orderItemsInOrder = []
        for orderItem in OrderItem.objects.all():
            if orderItem.order.orderNumber == self._order.orderNumber:
                orderItemsInOrder.append(orderItem)
        return orderItemsInOrder

    def getOrder(self):
        return self._order


def getAllOrderDetails(orders):
    allOrderDetailsList = []
    for order in orders:
        orderDetail = OrderDetails(order)
        allOrderDetailsList.append(orderDetail)
    return allOrderDetailsList


def getAllFoodContextDict():
    allOnePriceFood = getAllOnePriceFoodCategoriesWithFood()
    allTwoPriceFood = getAllTwoPriceFoodCategoriesWithFood()

    context = {
        "onePriceFoods": allOnePriceFood,
        "twoPriceFoods": allTwoPriceFood,
        "toppings": Topping.objects.all(),
        "specialPizza": SPECIAL_PIZZA,
    }
    return context


def getUserDependentContextDict(userOrder, currentPizza, pizzasToToppingsInOrder):
    context = {
        "order": FoodOrderItem.objects.filter(order=userOrder),
        "total": getTotalOrderPrice(userOrder),
        "pizzasToToppingsInOrder": pizzasToToppingsInOrder,
        "currentPizza": currentPizza
    }
    return context
