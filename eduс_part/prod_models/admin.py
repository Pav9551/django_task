from django.contrib import admin

# Register your models here.

from .models import Product, Lesson, Group, UserProduct

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)
admin.site.register(UserProduct)
