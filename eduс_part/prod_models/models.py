from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_users_per_group = models.PositiveIntegerField()
    max_users_per_group = models.PositiveIntegerField()
    def __str__(self):
        return f' {self.name}'

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    video_URL = models.URLField()
    def __str__(self):
        return f'{self.name} - {self.product.name}'

class UserProduct(models.Model):
    # Пользователь
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_products')
    # Продукт
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_products')
    # Дата и время покупки
    purchase_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

class Group(models.Model):
    product = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='educ_groups')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


