from orders.models import Pasta, RegularPizza, SicilianPizza, Sub, DinnerPlatter, Salad


class OnePriceFoodRenderer:
    def __init__(self, foodCateg):
        self.foodCateg = foodCateg
        self.categoryName = foodCateg.category
        self.allFoodInCategory = []

    def getFoodInCategory(self):
        for food in self.foodCateg.objects.all():
            self.allFoodInCategory.append(food)
        #return self.allFoodInCategory


# def listAllOnePriceFood():
#     allOnePriceFood = []
#     for x in [Pasta, Salad]:
#         r = OnePriceFoodRenderer(x)
#         r.getFoodInCategory()
#         allOnePriceFood.append(r)
#     return allOnePriceFood


class NumbersAndColours:
    def __init__(self, number):
        self.number = number
        self.colours = []

    def getColours(self):
        for c in ["yellow", "red", "green"]:
            self.colours.append(c)

    def __iter__(self):
        return iter(self.colours)


def listAllOnePriceFood():
    allOnePriceFood = []
    for number in ["one", "two", "three"]:
        nac = NumbersAndColours(number)
        nac.getColours()
        allOnePriceFood.append(nac)
    return allOnePriceFood




