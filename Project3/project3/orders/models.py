from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=64, default='Name')

    def __str__(self):
        return f"{self.name}"


class OnePriceFood(Food):
    price = models.DecimalField(max_digits=4, decimal_places=2, null=True, default='0.00')

    def __str__(self):
        return f"{self.name} - {self.price}"


class TwoPriceFood(Food):
    smallPrice = models.DecimalField(max_digits=4, decimal_places=2, null=True, default='0.00')
    largePrice = models.DecimalField(max_digits=4, decimal_places=2, null=True, default='0.00')

    def __str__(self):
        return f"{self.name} - {self.smallPrice} - {self.largePrice}"


class SicilianPizza(TwoPriceFood):
    pass


class RegularPizza(TwoPriceFood):
    pass


class Topping(Food):
    pass


class Sub(TwoPriceFood):
    pass


class Pasta(OnePriceFood):
    pass


class Salad(OnePriceFood):
    pass


class DinnerPlatter(TwoPriceFood):
    pass
