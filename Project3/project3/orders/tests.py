from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.

from .models import OnePriceFood, TwoPriceFood, Salad, RegularPizza, Topping, FoodOrderItem, Order, ToppingOrderItem
from .helpers import PizzaOrderHandler


pizzaOrderHandler = PizzaOrderHandler.PizzaOrderHandler()


class ModelsTestCase(TestCase):
    def setUp(self):
        OnePriceFood.objects.create(name="Pasta", price="1.10")
        TwoPriceFood.objects.create(name="DinnerPlatter", smallPrice="1.00", largePrice="1.20")
        Salad.objects.create(name="GardenSalad", category="Salad")

    def test_returnOnePriceFoodPrice_returnCorrectly(self):
        pasta = OnePriceFood.objects.get(name="Pasta")
        self.assertEqual("1.10", str(pasta.price))

    def test_returnTwoPriceFoodPrices_returnCorrectly(self):
        dinnerPlatter = TwoPriceFood.objects.get(name="DinnerPlatter")
        self.assertEqual("1.00", str(dinnerPlatter.smallPrice))
        self.assertEqual("1.20", str(dinnerPlatter.largePrice))

    def test_returnSaladCategory_returnCorrectly(self):
        gardenSalad = Salad.objects.get(name="GardenSalad")
        self.assertEqual("Salad", gardenSalad.category)

class PizzaOrderHandlerTestCase(TestCase):
    def setUp(self):
        RegularPizza.objects.create(name="2 toppings", category="RegularPizza", smallPrice="15.20", largePrice="21.95")
        Topping.objects.create(name="Mushrooms", category="Topping")
        user = User.objects.create_user(username="username")
        order = Order.objects.create(user=user, orderNumber="1")
        FoodOrderItem.objects.create(order=order, category="RegularPizza", name="3 toppings", isPizza=True, price="21.95")
      
    def test_getToppingAllowanceOfTwoToppingsPizza_twoReturned(self):
        twoToppingsPizza = RegularPizza.objects.get(name="2 toppings")
        toppingAllowance = pizzaOrderHandler.getInitialToppingAllowance(twoToppingsPizza.name)
        self.assertEqual(2, toppingAllowance)

    def test_addToppingToPizza(self):
        pizzaToTop = RegularPizza.objects.get(name="2 toppings")
        user = User.objects.get(username="username")
        order = Order.objects.get(orderNumber="1", user=user)
        pizzaOrderHandler.createPizzaOrderItem(order=order, category=pizzaToTop.category, name=pizzaToTop.name, price="21.95")
        pizzaOrderItem = FoodOrderItem.objects.get(order=order, name="2 toppings")
        self.assertEqual(pizzaOrderItem, pizzaOrderHandler.getCurrentPizza())

        toppingToAdd = Topping.objects.get(name="Mushrooms")
        self.assertEqual("Mushrooms", toppingToAdd.name)
        self.assertEqual("Topping", toppingToAdd.category)
        self.assertEqual(pizzaOrderHandler.getCurrentPizza(), pizzaOrderItem)
        self.assertEqual(True, pizzaOrderHandler.isCurrentPizzaToppable())

        foodItem = FoodOrderItem.objects.get(name="2 toppings")
        self.assertEqual(pizzaOrderHandler.getCurrentPizza(), foodItem)

        self.assertTrue(pizzaOrderHandler.pizza)

        pizzaOrderHandler.addTopping(toppingToAdd.category, toppingToAdd.name)

        #remainingToppingAllowance = pizzaOrderHandler.getRemainingToppingAllowance()
       # self.assertEqual(1, remainingToppingAllowance)


