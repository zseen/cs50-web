from django.db.models import Sum
from orders.models import Order, OrderItem, OrderCounter, ToppingOrderItem, Topping, FoodOrderItem
from .orderState import OrderState
from .WebpageRenderer import getAllOnePriceFoodCategoriesWithFood, getAllTwoPriceFoodCategoriesWithFood


def createNewOrderForUser(user):
    orderCounter = getOrderCounter()
    newUserOrder = Order(user=user, orderNumber=orderCounter.counter)
    newUserOrder.save()
    return newUserOrder


def getOrderCounter():
    orderCounter = OrderCounter.objects.first()
    if not orderCounter:
        orderCounter = OrderCounter(counter=1)

    currentOrderCounter = orderCounter
    orderCounter.counter += 1
    orderCounter.save()
    return currentOrderCounter


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
        "toppings": Topping.objects.all()
    }
    return context


def getUserDependentContextDict(userOrder, currentPizza, pizzasToToppingsInOrder):
    context = {
        "order": FoodOrderItem.objects.filter(order=userOrder),
        "total": getTotalOrderPrice(userOrder),
        "pizzasToToppingsInOrder":pizzasToToppingsInOrder,
        "currentPizza": currentPizza
    }
    return context
