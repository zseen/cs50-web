from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=64, default='SOME STRING')


class OnePriceFood(Food):
    price = models.DecimalField(max_digits=4, decimal_places=2, null= True, default='SOME STRING')


class TwoPriceFood(Food):
    smallPrice = models.DecimalField(max_digits=4, decimal_places=2, null= True, default='SOME STRING')
    largePrice = models.DecimalField(max_digits=4, decimal_places=2, null= True, default='SOME STRING')


class SicilianPizza(TwoPriceFood):
    def __str__(self):
        return f"{self.name} - {self.smallPrice} - {self.largePrice}"


class RegularPizza(TwoPriceFood):
    def __str__(self):
        return f"{self.name} - {self.smallPrice} - {self.largePrice}"


class Topping(Food):
    def __str__(self):
        return f"{self.name}"


class Sub(TwoPriceFood):
    def __str__(self):
        return f"{self.name} - {self.smallPrice} -{self.largePrice}"


class Pasta(OnePriceFood):
    def __str__(self):
        return f"{self.name} - {self.price}"


class Salad(OnePriceFood):
    def __str__(self):
        return f"{self.name} - {self.price}"


class DinnerPlatter(TwoPriceFood):
    def __str__(self):
        return f"{self.name} - {self.smallPrice} - {self.largePrice}"