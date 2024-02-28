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

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    video_URL = models.URLField()

class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='educ_groups')
    name = models.CharField(max_length=100)

