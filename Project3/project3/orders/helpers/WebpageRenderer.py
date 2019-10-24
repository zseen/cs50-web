from orders.models import Pasta, RegularPizza, SicilianPizza, Sub, DinnerPlatter, Salad, OnePriceFood


class OnePriceFoodRenderer:
    def __init__(self, foodCateg):
        self.foodCategory = foodCateg
        self.allFoodInCategory = []

    def getFoodInCategory(self):
        for food in self.foodCategory.objects.all():
            self.allFoodInCategory.append(food)

    def __iter__(self):
        return iter(self.allFoodInCategory)


class TwoPriceFoodRenderer:
    def __init__(self, foodCateg):
        self.foodCategory = foodCateg
        self.allFoodInCategory = []

    def getFoodInCategory(self):
        for food in self.foodCategory.objects.all():
            self.allFoodInCategory.append(food)

    def __iter__(self):
        return iter(self.allFoodInCategory)


def listAllOnePriceFood():
    allOnePriceFood = []
    for foodCategory in [Pasta, Salad]:
        onePriceFoods = OnePriceFoodRenderer(foodCategory)
        onePriceFoods.getFoodInCategory()
        allOnePriceFood.append(onePriceFoods)
    return allOnePriceFood

def listAllTwoPriceFood():
    allTwoPriceFood = []
    for foodCategory in [RegularPizza, SicilianPizza, Sub, DinnerPlatter]:
        twoPriceFoods = TwoPriceFoodRenderer(foodCategory)
        twoPriceFoods.getFoodInCategory()
        allTwoPriceFood.append(twoPriceFoods)
    return allTwoPriceFood

