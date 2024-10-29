# inventory/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Import the User model
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'inventory/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            # Attempt to authenticate using username
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                # If not found, try to authenticate using email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            if user:
                login(request, user)
                return redirect('product_list')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'inventory/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


@csrf_exempt
@login_required
def product_create_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        if not all([name, price, quantity]):
            return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields.'})

        try:
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                quantity=quantity
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def product_update_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        if not all([product_id, name, price, quantity]):
            return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields.'})

        try:
            product = get_object_or_404(Product, id=product_id)
            product.name = name
            product.description = description
            product.price = price
            product.quantity = quantity
            product.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def product_delete_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def product_list_ajax(request):
    if request.method == 'GET':
        # Get search parameters
        search_name = request.GET.get('search_name', '').strip()
        search_description = request.GET.get('search_description', '').strip()

        # Get sort parameters
        sort_by = request.GET.get('sort_by', 'id')  # Default sort by id
        order = request.GET.get('order', 'asc')  # Default ascending

        # Build queryset
        products = Product.objects.all()

        if search_name or search_description:
            products = products.filter(
                Q(name__icontains=search_name) | Q(description__icontains=search_description)
            )

        # Handle sorting
        if sort_by in ['price', 'quantity']:
            if order == 'desc':
                sort_by = '-' + sort_by
            products = products.order_by(sort_by)
        else:
            products = products.order_by('id')  # Default sort

        # Serialize data
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'quantity': product.quantity,
            })

        return JsonResponse({'status': 'success', 'products': products_data})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
