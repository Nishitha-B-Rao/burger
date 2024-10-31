# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'is_available']

class CustomUserCreationForm(UserCreationForm):
    pass  # Uses the default fields of Django's UserCreationForm
