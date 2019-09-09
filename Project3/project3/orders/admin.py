from django.contrib import admin
from .models import SicilianPizza, RegularPizza, Sub, DinnerPlatter, Salad, Topping, Pasta, OrderItem, Order


admin.site.register(SicilianPizza)
admin.site.register(RegularPizza)
admin.site.register(Sub)
admin.site.register(DinnerPlatter)
admin.site.register(Salad)
admin.site.register(Topping)
admin.site.register(Pasta)

admin.site.register(OrderItem)
admin.site.register(Order)

