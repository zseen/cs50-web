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


def getAllOrderDetails(orders):
    allOrderDetailsList = []
    for order in orders:
        orderDetail = OrderDetails(order)
        allOrderDetailsList.append(orderDetail)
    return allOrderDetailsList


class PizzaOrderHandler:
    def __init__(self):
        self.pizza = None

    def getCurrentPizza(self):
        return self.pizza

    def createPizzaOrderItem(self, order, category, name, price):
        toppingAllowance = self.getToppingAllowance()
        self.pizza = OrderItem(order=order, category=category, name=name, price=price, toppingAllowance=toppingAllowance)
        self.pizza.save()

    def getToppingAllowance(self):
        toppingAllowance = 0
        if self.pizza.name == "1 topping":
            toppingAllowance = 1
        elif self.pizza.name == "2 toppings":
            toppingAllowance = 2
        elif self.pizza.name == "3 toppings":
            toppingAllowance = 3

        return toppingAllowance

    def decreaseToppingAllowance(self):
        self.pizza.toppingAllowance -= 1
        self.pizza.save()

    def getRemainingToppingAllowanceMessage(self):
        message = "You can add " + str(self.pizza.toppingAllowance) + " more topping(s)."
        if self.pizza.toppingAllowance == 0:
            message = "All toppings added!"
        return message


