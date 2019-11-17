from .PizzaOrderHandler import PizzaOrderHandler
from orders.models import FoodOrderItem


class FoodOrderItemWithToppings:
    def __init__(self, foodOrderItem, toppings):
        self.foodOrderItem = foodOrderItem
        self.toppings = toppings


class AllFoodsInUserOrder:
    def __init__(self, order):
        self._order = order
        self._allFoodsInUserOrder = self._getAllFoodsWithToppingsInUserOrder()

    def getOrder(self):
        return self._order

    def getAllFoodsInUserOrder(self):
        return self._allFoodsInUserOrder

    def _getAllFoodsWithToppingsInUserOrder(self):
        allFoodsInUserOrder = []
        pizzasToToppings = PizzaOrderHandler.getAllPizzasToToppingsInUserOrder(self._order)

        for pizza, toppings in pizzasToToppings.items():
            foodWithTopping = FoodOrderItemWithToppings(pizza, toppings)
            allFoodsInUserOrder.append(foodWithTopping)

        foodItems = self._getFoodOrderItemsInUserOrder()
        for foodItem in foodItems:
            if not foodItem.isPizza:
                foodWithTopping = FoodOrderItemWithToppings(foodItem, toppings=None)
                allFoodsInUserOrder.append(foodWithTopping)

        return allFoodsInUserOrder

    def _getFoodOrderItemsInUserOrder(self):
        orderItemsInOrder = []
        for orderItem in FoodOrderItem.objects.all():
            if orderItem.order.orderNumber == self._order.orderNumber:
                orderItemsInOrder.append(orderItem)
        return orderItemsInOrder


def getAllFoodsWithToppingsInUserOrder(order):
    return AllFoodsInUserOrder(order)


def getAllFoodsWithToppingsInSelectedUserOrders(orders):
    allFoodsWithToppingsInUserOrders = []

    for order in orders:
        allFoodsInUserOrder = getAllFoodsWithToppingsInUserOrder(order)
        allFoodsWithToppingsInUserOrders.append(allFoodsInUserOrder)

    return allFoodsWithToppingsInUserOrders
