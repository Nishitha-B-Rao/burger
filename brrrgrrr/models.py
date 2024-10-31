# models.py
from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CustomBurger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def calculate_total_price(self):
        self.total_price = sum(ingredient.price for ingredient in self.ingredients.all())
        self.save()
