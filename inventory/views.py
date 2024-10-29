# inventory/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


@csrf_exempt
def product_create_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

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
def product_update_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

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
