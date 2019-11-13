from .PizzaOrderHandler import PizzaOrderHandler
from .OrderUtils import OrderDetails


class FoodOrderItemWithToppings:
    def __init__(self):
        self.foodOrderItem = None
        self.toppings = []


class AllFoodInUserOrder:
    def __init__(self, order):
        self.order = order
        self.allFoodInUserOrder = []

    def getFoodItemsWithToppingsInUserOrder(self):
        pizzasToToppings = PizzaOrderHandler.getAllPizzasToToppingsInUserOrder(self.order)

        for pizza, topping in pizzasToToppings.items():
            foodWithTopping = FoodOrderItemWithToppings()
            foodWithTopping.foodOrderItem = pizza
            foodWithTopping.toppings = topping
            self.allFoodInUserOrder.append(foodWithTopping)

        orderDetails = OrderDetails(self.order)
        foodItems = orderDetails.getOrderItemsInOrder()
        for foodItem in foodItems:
            if not foodItem.isPizza:
                foodWithTopping = FoodOrderItemWithToppings()
                foodWithTopping.foodOrderItem = foodItem
                self.allFoodInUserOrder.append(foodWithTopping)

    def getOrder(self):
        return self.order


def getAllFoodWithToppingsInSelectedUserOrders(orders):
    allFoodWithToppingsInUserOrders = []

    for order in orders:
        allFoodInUserOrder = AllFoodInUserOrder(order)
        allFoodInUserOrder.getFoodItemsWithToppingsInUserOrder()
        allFoodWithToppingsInUserOrders.append(allFoodInUserOrder)

    return allFoodWithToppingsInUserOrders
