from orders.models import Order, OrderItem, OrderCounter, ToppingOrderItem, FoodOrderItem
from enum import Enum


class PizzaCategory(Enum):
    REGULAR_PIZZA = "Regular pizza"
    SICILIAN_PIZZA = "Sicilian pizza"


class PizzaName(Enum):
    ONE_TOPPING = "1 topping"
    TWO_TOPPINGS = "2 toppings"
    THREE_TOPPINGS = "3 toppings"


class PizzaOrderHandler:
    def __init__(self):
        self.pizza = None

    def getCurrentPizza(self):
        return self.pizza

    def createPizzaOrderItem(self, order, category, name, price):
        toppingAllowance = self.getInitialToppingAllowance(name)
        self.pizza = FoodOrderItem(order=order, category=category, name=name, price=price,
                               toppingAllowance=toppingAllowance)
        self.pizza.save()

    def decreaseToppingAllowance(self):
        if self.pizza.toppingAllowance > 0:
            self.pizza.toppingAllowance -= 1
            self.pizza.save()

    def getRemainingToppingAllowance(self):
        return self.pizza.toppingAllowance

    def isCurrentPizzaToppable(self):
        return self.pizza.toppingAllowance > 0

    def increaseToppingAllowance(self):
        self.pizza.toppingAllowance += 1

    @staticmethod
    def getAllPizzasToToppingsInOrder(order):
        pizzaToToppings = dict()
        for pizzaCategory in [PizzaCategory.REGULAR_PIZZA.value, PizzaCategory.SICILIAN_PIZZA.value]:
            pizzas = FoodOrderItem.objects.filter(order=order, category=pizzaCategory)
            for pizza in pizzas:
                pizzaToToppings[pizza] = ToppingOrderItem.objects.filter(foodOrderItem=pizza)

        return pizzaToToppings

    @staticmethod
    def getInitialToppingAllowance(pizzaName):
        toppingAllowance = 0
        if pizzaName == PizzaName.ONE_TOPPING.value:
            toppingAllowance = 1
        elif pizzaName == PizzaName.TWO_TOPPINGS.value:
            toppingAllowance = 2
        elif pizzaName == PizzaName.THREE_TOPPINGS.value:
            toppingAllowance = 3

        return toppingAllowance

