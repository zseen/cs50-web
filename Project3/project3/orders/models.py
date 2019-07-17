from django.db import models


class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    smallPrice = models.DecimalField(max_digits=4, decimal_places=2)
    largePrice = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.smallPrice} - {self.largePrice}"


class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    smallPrice = models.DecimalField(max_digits=4, decimal_places=2)
    largePrice = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.smallPrice} - {self.largePrice}"


class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Sub(models.Model):
    name = models.CharField(max_length=64)
    smallPrice = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    largePrice = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.smallPrice} -{self.largePrice}"


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    smallPrice = models.DecimalField(max_digits=4, decimal_places=2)
    largePrice = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.smallPrice} - {self.largePrice}"