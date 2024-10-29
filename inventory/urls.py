# inventory/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ajax/product/create/', views.product_create_ajax, name='product_create_ajax'),
    path('ajax/product/update/', views.product_update_ajax, name='product_update_ajax'),
    path('ajax/product/delete/', views.product_delete_ajax, name='product_delete_ajax'),
    path('ajax/product/list/', views.product_list_ajax, name='product_list_ajax'),
]
