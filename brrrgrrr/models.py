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
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def calculate_total_price(self):
        # Calculate total price based on associated ingredients
        self.total_price = sum(
            item.quantity * item.ingredient.price for item in self.ingredients.all()
        )
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Burger - ${self.total_price}"


class CustomBurgerIngredient(models.Model):
    burger = models.ForeignKey(CustomBurger, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.ingredient.name} for {self.burger}"

