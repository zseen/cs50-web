from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    name = models.CharField(max_length=64, default='Name')
    category = models.CharField(max_length=64, default='Category')

    def __str__(self):
        return f"{self.name} - {self.category}"


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


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    number=models.IntegerField()
    category=models.CharField(max_length=64,null=True)
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price} "