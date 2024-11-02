# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    

class CustomUserCreationForm(UserCreationForm):
    pass  # Uses the default fields of Django's UserCreationForm
