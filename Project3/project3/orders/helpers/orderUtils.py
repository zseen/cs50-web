from django.db.models import Sum
from orders.models import Order, OrderItem, OrderCounter, ToppingOrderItem
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
        toppingAllowance = self.getInitialToppingAllowance(name)
        self.pizza = OrderItem(order=order, category=category, name=name, price=price,
                               toppingAllowance=toppingAllowance)
        self.pizza.save()

    def decreaseToppingAllowance(self):
        if self.pizza.toppingAllowance > 0:
            self.pizza.toppingAllowance -= 1
            self.pizza.save()

    def getRemainingToppingAllowanceMessage(self):
        message = "You can add " + str(self.pizza.toppingAllowance) + " more topping(s)."

        if self.pizza.name == "Cheese":
            message = ""
        elif self.pizza.toppingAllowance == 0:
            message = "All toppings added!"

        return message

    def canCurrentPizzaBeTopped(self):
        return self.pizza.toppingAllowance > 0

    def increaseToppingAllowance(self):
        self.pizza.toppingAllowance += 1

    @staticmethod
    def getAllPizzasToToppingsInOrder(order):
        regularPizzasInOrder = OrderItem.objects.filter(order=order, category="Regular pizza")
        sicilianPizzasInOrder = OrderItem.objects.filter(order=order, category="Sicilian pizza")

        pizzaToToppings = dict()
        for pizza in regularPizzasInOrder:
            pizzaToToppings[pizza] = ToppingOrderItem.objects.filter(orderItem=pizza)

        for pizza in sicilianPizzasInOrder:
            pizzaToToppings[pizza] = ToppingOrderItem.objects.filter(orderItem=pizza)

        return pizzaToToppings

    @staticmethod
    def getInitialToppingAllowance(pizzaName):
        toppingAllowance = 0
        if pizzaName == "1 topping":
            toppingAllowance = 1
        elif pizzaName == "2 toppings":
            toppingAllowance = 2
        elif pizzaName == "3 toppings":
            toppingAllowance = 3

        return toppingAllowance
