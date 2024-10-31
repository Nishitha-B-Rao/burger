# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customize-burger/', views.customize_burger, name='customize_burger'),

    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('ingredients/add/', views.add_or_edit_ingredient, name='add_ingredient'),
    path('ingredients/edit/<int:ingredient_id>/', views.add_or_edit_ingredient, name='edit_ingredient'),
    path('ingredients/delete/<int:pk>/', views.delete_ingredient, name='delete_ingredient'),
]
