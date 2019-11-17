from .PizzaOrderHandler import PizzaOrderHandler
from orders.models import FoodOrderItem


class FoodOrderItemWithToppings:
    def __init__(self):
        self.foodOrderItem = None
        self.toppings = []


class AllFoodsInUserOrder:
    def __init__(self, order):
        self._order = order
        self._allFoodsInUserOrder = []

    def getFoodOrderItemsInUserOrder(self):
        orderItemsInOrder = []
        for orderItem in FoodOrderItem.objects.all():
            if orderItem.order.orderNumber == self._order.orderNumber:
                orderItemsInOrder.append(orderItem)
        return orderItemsInOrder

    def getAllFoodsWithToppingsInUserOrder(self):
        pizzasToToppings = PizzaOrderHandler.getAllPizzasToToppingsInUserOrder(self._order)

        for pizza, topping in pizzasToToppings.items():
            foodWithTopping = FoodOrderItemWithToppings()
            foodWithTopping.foodOrderItem = pizza
            foodWithTopping.toppings = topping
            self._allFoodsInUserOrder.append(foodWithTopping)

        foodItems = self.getFoodOrderItemsInUserOrder()
        for foodItem in foodItems:
            if not foodItem.isPizza:
                foodWithTopping = FoodOrderItemWithToppings()
                foodWithTopping.foodOrderItem = foodItem
                self._allFoodsInUserOrder.append(foodWithTopping)

    def getOrder(self):
        return self._order

    def getAllFoodsInUserOrder(self):
        return self._allFoodsInUserOrder


def getAllFoodsWithToppingsInSelectedUserOrders(orders):
    allFoodsWithToppingsInUserOrders = []

    for order in orders:
        allFoodsInUserOrder = AllFoodsInUserOrder(order)
        allFoodsInUserOrder.getAllFoodsWithToppingsInUserOrder()
        allFoodsWithToppingsInUserOrders.append(allFoodsInUserOrder)

    return allFoodsWithToppingsInUserOrders
