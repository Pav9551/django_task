from django.urls import path, include
from .models import Product
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name','start_date','cost','lessoncount']

