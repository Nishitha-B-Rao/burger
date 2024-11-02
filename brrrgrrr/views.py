from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from . models import Ingredient, CustomBurger, CustomBurgerIngredient, Order
from . forms import IngredientForm
from django.contrib import messages
import json
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

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


@login_required
def place_order(request):
    if request.method == 'POST':
        burger_data = request.POST.get('burger_data')
        if not burger_data:
            messages.error(request, 'No ingredients selected!')
            return redirect('customize_burger')
            
        try:
            # Create the burger
            burger = CustomBurger.objects.create(user=request.user)
            
            # Parse the burger data and create ingredients
            ingredients_data = json.loads(burger_data)
            for item in ingredients_data:
                ingredient = Ingredient.objects.get(id=item['ingredientId'])  # Changed from 'id' to 'ingredientId'
                CustomBurgerIngredient.objects.create(
                    burger=burger,
                    ingredient=ingredient,
                    quantity=item['quantity']
                )
            
            burger.calculate_total_price()
            
            # Create the order
            order = Order.objects.create(
                user=request.user,
                burger=burger,
                status='PENDING'
            )
            
            return redirect('order_confirmation', order_id=order.id)
            
        except json.JSONDecodeError:
            messages.error(request, 'Invalid burger data format!')
        except Ingredient.DoesNotExist:
            messages.error(request, 'One or more ingredients not found!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        
        return redirect('customize_burger')
    
    return redirect('customize_burger')

@login_required
def order_confirmation(request, order_id):
    order = Order.objects.select_related('burger', 'user').get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get filter parameters from request
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', 'all')
    search_query = request.GET.get('search', '')

    # Base queryset
    orders = Order.objects.select_related('user', 'burger').prefetch_related(
        'burger__ingredients__ingredient'
    ).order_by('-created_at')

    # Apply filters
    if status_filter:
        orders = orders.filter(status=status_filter)

    if date_filter == 'today':
        orders = orders.filter(created_at__date=timezone.now().date())
    elif date_filter == 'week':
        week_ago = timezone.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=week_ago)

    if search_query:
        orders = orders.filter(
            Q(user__username__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
        'current_date': date_filter,
        'search_query': search_query,
    }
    return render(request, 'orders_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order_id} status updated to {new_status}')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
    
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def order_details(request, order_id):
    try:
        order = Order.objects.select_related('user', 'burger').prefetch_related(
            'burger__ingredients__ingredient'
        ).get(id=order_id)
        
        context = {
            'order': order,
            'status_choices': Order.STATUS_CHOICES,
        }
        return render(request, 'order_details.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('admin_dashboard')
    
@login_required
def my_orders(request):
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', 'all')
    
    # Get orders for the current user
    orders = Order.objects.select_related('burger').prefetch_related(
        'burger__ingredients__ingredient'
    ).filter(user=request.user).order_by('-created_at')
    
    # Apply status filter if specified
    if status_filter:
        orders = orders.filter(status=status_filter)
        
    # Apply date filter
    if date_filter == 'today':
        orders = orders.filter(created_at__date=timezone.now().date())
    elif date_filter == 'week':
        week_ago = timezone.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=week_ago)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
        'current_date': date_filter,
    }
    return render(request, 'myorders.html', context)