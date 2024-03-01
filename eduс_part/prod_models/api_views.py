from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
