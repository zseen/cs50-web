from django.test import TestCase
from django.contrib.auth.models import User
from .models import OnePriceFood, TwoPriceFood, Salad, RegularPizza, Topping, FoodOrderItem, Order
from .helpers import PizzaOrderHandler

pizzaOrderHandler = PizzaOrderHandler.PizzaOrderHandler()


class ModelsTestCase(TestCase):
    def setUp(self):
        OnePriceFood.objects.create(name="BakedZiti", price="1.10")
        TwoPriceFood.objects.create(name="Antipasto", smallPrice="1.00", largePrice="1.20")
        Salad.objects.create(name="GardenSalad", category="Salad")

    def test_getOnePriceFoodByName_getItsPrice_priceMatchesSetUp(self):
        bakedZiti = OnePriceFood.objects.get(name="BakedZiti")
        self.assertEqual("1.10", str(bakedZiti.price))

    def test_getTwoPriceFoodByName_getBothPrices_pricesMatchSetUp(self):
        antiPasto = TwoPriceFood.objects.get(name="Antipasto")
        self.assertEqual("1.00", str(antiPasto.smallPrice))
        self.assertEqual("1.20", str(antiPasto.largePrice))

    def test_getSaladByName_getItsCategory_categoryMatchesSetUp(self):
        gardenSalad = Salad.objects.get(name="GardenSalad")
        self.assertEqual("Salad", gardenSalad.category)


class PizzaOrderHandlerTestCase(TestCase):
    def setUp(self):
        RegularPizza.objects.create(name="2 toppings", category="RegularPizza", smallPrice="15.20", largePrice="21.95")
        Topping.objects.create(name="Mushrooms", category="Topping")
        user = User.objects.create_user(username="username")
        Order.objects.create(user=user, orderNumber="1")

    @staticmethod
    def createPizzaOrderItem():
        pizzaToTop = RegularPizza.objects.get(name="2 toppings")
        user = User.objects.get(username="username")
        order = Order.objects.get(orderNumber="1", user=user)
        pizzaOrderHandler.createPizzaOrderItem(order=order, category=pizzaToTop.category, name=pizzaToTop.name,
                                               price="21.95")

        pizzaOrderItem = FoodOrderItem.objects.get(order=order, name="2 toppings")
        return pizzaOrderItem

    def test_getInitialToppingAllowance_twoToppingsPizza_equalsTwo(self):
        twoToppingsPizza = RegularPizza.objects.get(name="2 toppings")
        toppingAllowance = pizzaOrderHandler.getInitialToppingAllowance(twoToppingsPizza.name)
        self.assertEqual(2, toppingAllowance)

    def test_createPizzaOrderItem_callTestCaseCreatePizzaOrderItem_newlyCreatedPizzaIsCurrentPizza(self):
        pizzaOrderItem = PizzaOrderHandlerTestCase.createPizzaOrderItem()
        self.assertEqual(pizzaOrderItem, pizzaOrderHandler.getCurrentPizza())

    def test_addToppingToTwoToppingsPizza_topTwice_zeroRemainingToppingAllowance(self):
        pizzaToTop = PizzaOrderHandlerTestCase.createPizzaOrderItem()
        self.assertEqual(pizzaToTop, pizzaOrderHandler.getCurrentPizza())

        originalToppingAllowance = pizzaOrderHandler.getInitialToppingAllowance(pizzaToTop.name)
        self.assertEqual(2, originalToppingAllowance)

        toppingToAdd = Topping.objects.get(name="Mushrooms")
        pizzaOrderHandler.addTopping(toppingToAdd.category, toppingToAdd.name)

        remainingToppingAllowance = pizzaOrderHandler.getRemainingToppingAllowance()
        self.assertEqual(1, remainingToppingAllowance)

        pizzaOrderHandler.addTopping(toppingToAdd.category, toppingToAdd.name)
        remainingToppingAllowance = pizzaOrderHandler.getRemainingToppingAllowance()
        self.assertEqual(0, remainingToppingAllowance)
