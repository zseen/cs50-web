from django.db.models import Sum
from orders.models import Order, OrderItem, OrderCounter
from .orderState import OrderState


def createNewOrderForUser(user):
    orderCounter = OrderCounter.objects.first()
    newUserOrder = Order(user=user, orderNumber=orderCounter.counter)
    newUserOrder.save()
    orderCounter.counter += 1
    orderCounter.save()
    return newUserOrder


def getCurrentOrderForUser(user):
    try:
        order = Order.objects.get(user=user, status=OrderState.INITIATED.value)
    except Order.DoesNotExist:
        order = createNewOrderForUser(user)
    return order


def getTotalOrderPrice(order):
    return OrderItem.objects.filter(order=order).aggregate(Sum('price'))['price__sum']


class FoodInOrderFinder:
    def __init__(self, order):
        self._order = order
        self._foodInOrder = []

    def findAllFoodInOrder(self):
        for orderItem in OrderItem.objects.all():
            if orderItem.order.orderNumber == self._order.orderNumber:
                self._foodInOrder.append(orderItem)

    def getFoodInOrder(self):
        return self._foodInOrder

    def getOrder(self):
        return self._order


class FoodInAllOrdersFinder:
    def __init__(self):
        self._foodToAllOrdersList = []

    def _findFoodInAllOrders(self, orders):
        for order in orders:
            userOrder = FoodInOrderFinder(order)
            userOrder.findAllFoodInOrder()
            self._foodToAllOrdersList.append(userOrder)

    def getFoodToAllOrdersList(self, orders):
        self._findFoodInAllOrders(orders)
        return self._foodToAllOrdersList
