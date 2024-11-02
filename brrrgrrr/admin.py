from django.contrib import admin
from .models import Ingredient, Order, CustomBurger

admin.site.register(Ingredient)
admin.site.register(Order)
admin.site.register(CustomBurger)
