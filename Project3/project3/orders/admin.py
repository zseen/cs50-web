from django.contrib import admin
from .models import SicilianPizza, RegularPizza, Subs, DinnerPlatters, Salads, Toppings, Pasta


# Register your models here.
admin.site.register(SicilianPizza)
admin.site.register(RegularPizza)
admin.site.register(Subs)
admin.site.register(DinnerPlatters)
admin.site.register(Salads)
admin.site.register(Toppings)
admin.site.register(Pasta)
