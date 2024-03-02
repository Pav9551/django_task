from .models import Product, UserProduct, Group, Lesson
from .serializers import ProductSerializer, UserProductSerializer
from rest_framework import viewsets
from rest_framework import generics

# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class UserProductViewSet(viewsets.ModelViewSet):
    user = Group.get_user()
    print('UserProductViewSet')
    queryset = UserProduct.objects.filter(user=user)
    serializer_class = UserProductSerializer





