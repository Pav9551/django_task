from django.contrib import admin

# Register your models here.

from .models import Product, Lesson, Group

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)
