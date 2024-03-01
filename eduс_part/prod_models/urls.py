from django.urls import path
from prod_models import views
app_name = 'prod_models'
urlpatterns = [
    path('', views.main_view, name ='index'),
    path('empty', views.empty_view, name = 'empty'),
    path('product/<int:id>/', views.user_product_view, name = 'product'),
]

