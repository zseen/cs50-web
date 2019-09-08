from django.db import models
from django.contrib.auth.models import User


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
    category = models.CharField(max_length=64, default='Sicilian pizza')


class RegularPizza(TwoPriceFood):
    category = models.CharField(max_length=64, default='Regular pizza')


class Topping(Food):
    category = models.CharField(max_length=64, default='Topping')


class Sub(TwoPriceFood):
    category = models.CharField(max_length=64, default='Sub')


class Pasta(OnePriceFood):
    category = models.CharField(max_length=64, default='Pasta')


class Salad(OnePriceFood):
    category = models.CharField(max_length=64, default='Salad')


class DinnerPlatter(TwoPriceFood):
    category = models.CharField(max_length=64, default='Dinner platter')


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    number=models.IntegerField()
    category=models.CharField(max_length=64,null=True)
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price} "