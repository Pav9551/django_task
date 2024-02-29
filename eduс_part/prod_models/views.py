from django.shortcuts import render
from .models import Product
# Create your views here.
def main_view(request):
    products = Product.objects.all()
    return render(request, 'prod_models_app/index.html', context={'products': products})
