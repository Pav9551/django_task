from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
# Create your views here.
def main_view(request):
    products = Product.objects.all()
    return render(request, 'prod_models_app/index.html', context={'products': products})
def empty_view(request):
    products = Product.objects.all()
    return render(request, 'prod_models_app/empty.html', context={'products': products})
def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'prod_models_app/product.html', context={'product': product})
def user_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        return redirect('/')
    else:
        return render(request, 'prod_models_app/product.html', context={'product': product})
