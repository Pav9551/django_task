from django.urls import path
from prod_models import views
app_name = 'prod_models'
urlpatterns = [
    path('', views.main_view),
]

