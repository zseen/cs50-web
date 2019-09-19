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


def getOrderItemsToAllOrdersList(orders):
    allOrderDetailsList = []
    for order in orders:
        orderDetail = OrderDetails(order)
        allOrderDetailsList.append(orderDetail)
    return allOrderDetailsList
