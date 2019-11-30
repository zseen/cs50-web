from django.test import TestCase


# Create your tests here.

from .models import Food, OnePriceFood, FoodOrderItem, ToppingOrderItem, Order, Pasta, DinnerPlatter, RegularPizza, TwoPriceFood


class ModelsTestCase(TestCase):
    def setup(self):
        food = Food.objects.create(name="food")
        onePriceFood = OnePriceFood.objects.create(name="onePriceFood", price="1.1")
        twoPriceFood = TwoPriceFood.objects.create(name="twoPriceFood", smallPrice="1.0", largePrice="1.2")
        pasta = Pasta.objects.create(category="pasta")

    def test_returnFoodName_foodNameReturnedCorrectly(self):
        foodName = Food.objects.get(name="food")
        self.assertEqual("food", foodName)


