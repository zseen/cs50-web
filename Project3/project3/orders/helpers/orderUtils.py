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


class FoodInOrderLister:
    def __init__(self, order):
        self.order = order
        self.foodInOrder = []

    def _findFoodInOrder(self):
        for orderItem in OrderItem.objects.all():
            if orderItem.order.orderNumber == self.order.orderNumber:
                self.foodInOrder.append(orderItem)

    def getFoodInOrder(self):
        self._findFoodInOrder()
        return self.foodInOrder

    def getOrder(self):
        return self.order


class FoodToAllOrdersLister:
    def __init__(self):
        self._foodToAllOrdersList = []

    def _findFoodToAllOrders(self, orders):
        for order in orders:
            ord = FoodInOrderLister(order)
            ord.getFoodInOrder()
            self._foodToAllOrdersList.append(ord)

    def getFoodToAllOrdersList(self, orders):
        self._findFoodToAllOrders(orders)
        return self._foodToAllOrdersList





