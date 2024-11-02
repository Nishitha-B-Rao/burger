from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from . models import Ingredient
from . forms import IngredientForm

def home(request):
    return render(request, 'home.html')

# Check if user is an admin
def is_admin(user):
    return user.is_staff

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customize_burger')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect admin to ingredient list page, others to customize_burger page
            if user.is_staff:
                return redirect('ingredient_list')
            else:
                return redirect('customize_burger')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# List all ingredients for admin management
@login_required
@user_passes_test(is_admin)
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_list.html', {'ingredients': ingredients})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# Add or edit ingredient
@login_required
@user_passes_test(is_admin)
def add_ingredient(request):
    form = IngredientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ingredient_list')
    return render(request, 'ingredient_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    form = IngredientForm(request.POST or None, instance=ingredient)
    if request.method == 'POST' and form.is_valid():
        print("Form valid. Checkbox value:", form.cleaned_data['is_available'])
        form.save()
        return redirect('ingredient_list')
    return render(request, 'ingredient_form.html', {'form': form})


# Delete an ingredient
@login_required
@user_passes_test(is_admin)
def delete_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient_list')
    return render(request, 'delete_ingredient.html', {'ingredient': ingredient})

@login_required
def customize_burger(request):
    ingredients = Ingredient.objects.filter(is_available=True)
    return render(request, 'customize_burger.html', {'ingredients': ingredients})

# Admin ingredient management views
@login_required
@user_passes_test(is_admin)
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_list.html', {'ingredients': ingredients})
