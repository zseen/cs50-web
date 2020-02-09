from orders.models import Pasta, RegularPizza, SicilianPizza, Sub, DinnerPlatter, Salad, OnePriceFood

ONE_PRICE_FOODS = [Pasta, Salad]
TWO_PRICE_FOODS = [RegularPizza, SicilianPizza, Sub, DinnerPlatter]


class FoodSection:
    def __init__(self, foodCategory):
        self.foodCategory = foodCategory
        self.allFoodInCategory = list(self.foodCategory.objects.all())


def getFoodSectionList(foodCategories):
    return [FoodSection(foodCategory) for foodCategory in foodCategories]


def getAllOnePriceFoodCategoriesWithFood():
    return getFoodSectionList(ONE_PRICE_FOODS)


def getAllTwoPriceFoodCategoriesWithFood():
    return getFoodSectionList(TWO_PRICE_FOODS)
