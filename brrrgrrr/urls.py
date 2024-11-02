# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customize-burger/', views.customize_burger, name='customize_burger'),

    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('ingredients/add/', views.add_ingredient, name='add_ingredient'),
    path('ingredients/edit/<int:ingredient_id>/', views.edit_ingredient, name='edit_ingredient'),
    path('ingredients/delete/<int:pk>/', views.delete_ingredient, name='delete_ingredient'),

     path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
     path('orders/', views.admin_dashboard, name='admin_dashboard'),
    path('orders/<int:order_id>/', views.order_details, name='admin_order_details'),
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
