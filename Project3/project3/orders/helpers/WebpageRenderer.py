from orders.models import Pasta, RegularPizza, SicilianPizza, Sub, DinnerPlatter, Salad, OnePriceFood
from enum import Enum


class FoodPriceCategory(Enum):
    ONE_PRICE_FOODS = [Pasta, Salad]
    TWO_PRICE_FOODS = [RegularPizza, SicilianPizza, Sub, DinnerPlatter]


class FoodCategoryRenderer:
    def __init__(self, foodCategory):
        self.foodCategory = foodCategory
        self.allFoodInCategory = list(self.foodCategory.objects.all())


def getCategoryAndFoodItemsList(foodPriceCategory):
    allFoodCategoriesWithFoodList = []
    for foodCategory in foodPriceCategory:
        foodCategoryRenderer = FoodCategoryRenderer(foodCategory)
        allFoodCategoriesWithFoodList.append(foodCategoryRenderer)
    return allFoodCategoriesWithFoodList


def getAllOnePriceFoodCategoriesWithFood():
    return getCategoryAndFoodItemsList(FoodPriceCategory.ONE_PRICE_FOODS.value)


def getAllTwoPriceFoodCategoriesWithFood():
    return getCategoryAndFoodItemsList(FoodPriceCategory.TWO_PRICE_FOODS.value)
