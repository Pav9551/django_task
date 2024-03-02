from django.urls import path, include
from .models import Product, UserProduct, Lesson
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name','start_date','cost','lessoncount']

class UserProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProduct
        fields =  ['product','purchase_date']

from .models import Lesson


