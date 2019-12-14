from django.test import TestCase
from django.contrib.auth.models import User
from .models import OnePriceFood, TwoPriceFood, Salad, RegularPizza, Topping, FoodOrderItem, Order
from .helpers import PizzaOrderHandler

pizzaOrderHandler = PizzaOrderHandler.PizzaOrderHandler()


class ModelsTestCase(TestCase):
    def setUp(self):
        OnePriceFood.objects.create(name="Pasta", price="1.10")
        TwoPriceFood.objects.create(name="DinnerPlatter", smallPrice="1.00", largePrice="1.20")
        Salad.objects.create(name="GardenSalad", category="Salad")

    def test_getOnePriceFoodByName_getItsPrice_priceMatchesSetUp(self):
        pasta = OnePriceFood.objects.get(name="Pasta")
        self.assertEqual("1.10", str(pasta.price))

    def test_getTwoPriceFoodByName_getBothPrices_pricesMatchSetUp(self):
        dinnerPlatter = TwoPriceFood.objects.get(name="DinnerPlatter")
        self.assertEqual("1.00", str(dinnerPlatter.smallPrice))
        self.assertEqual("1.20", str(dinnerPlatter.largePrice))

    def test_getSaladByName_getItsCategory_categoryMatchesSetUp(self):
        gardenSalad = Salad.objects.get(name="GardenSalad")
        self.assertEqual("Salad", gardenSalad.category)


class PizzaOrderHandlerTestCase(TestCase):
    def setUp(self):
        RegularPizza.objects.create(name="2 toppings", category="RegularPizza", smallPrice="15.20", largePrice="21.95")
        Topping.objects.create(name="Mushrooms", category="Topping")
        user = User.objects.create_user(username="username")
        order = Order.objects.create(user=user, orderNumber="1")
        FoodOrderItem.objects.create(order=order, category="RegularPizza", name="3 toppings", isPizza=True,
                                     price="21.95")

    def test_getToppingAllowance_twoToppingsPizza_equalsTwo(self):
        twoToppingsPizza = RegularPizza.objects.get(name="2 toppings")
        toppingAllowance = pizzaOrderHandler.getInitialToppingAllowance(twoToppingsPizza.name)
        self.assertEqual(2, toppingAllowance)

    def test_addToppingToTwoToppingsPizza_topTwice_zeroRemainingToppingAllowance(self):
        pizzaToTop = RegularPizza.objects.get(name="2 toppings")
        user = User.objects.get(username="username")
        order = Order.objects.get(orderNumber="1", user=user)
        pizzaOrderHandler.createPizzaOrderItem(order=order, category=pizzaToTop.category, name=pizzaToTop.name,
                                               price="21.95")

        pizzaOrderItem = FoodOrderItem.objects.get(order=order, name="2 toppings")
        self.assertEqual(pizzaOrderItem, pizzaOrderHandler.getCurrentPizza())

        self.assertEqual(True, pizzaOrderHandler.isCurrentPizzaToppable())

        toppingToAdd = Topping.objects.get(name="Mushrooms")
        pizzaOrderHandler.addTopping(toppingToAdd.category, toppingToAdd.name)
        remainingToppingAllowance = pizzaOrderHandler.getRemainingToppingAllowance()
        self.assertEqual(1, remainingToppingAllowance)

        pizzaOrderHandler.addTopping(toppingToAdd.category, toppingToAdd.name)
        remainingToppingAllowance = pizzaOrderHandler.getRemainingToppingAllowance()
        self.assertEqual(0, remainingToppingAllowance)
