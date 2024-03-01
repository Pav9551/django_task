from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Product, Lesson
from django.conf import settings

from django.db.models import Count
#функция подсчета уроков в проекте
def update_Product(instance):
    if instance.id is None:
        pass
    else:
        products = Product.objects.annotate(lesson_count=Count('prod_lessons'))
        result = []
        for product in products:
            item = {
                        'name': product.name,
                        'lesson_count': product.lesson_count,
                        'id': product.id
                    }
            curproduct = Product.objects.get(id=product.id)
            curproduct.lessoncount = product.lesson_count
            curproduct.save()
            result.append(item)
        print(result)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(**kwargs):
    print('Пользователь создан или изменен')

@receiver(post_save, sender=Product)
def post_save_product(**kwargs):
    print('Продукт создан или изменен')
@receiver(post_save, sender=Lesson)
def post_save_lesson(instance,**kwargs):
    update_Product(instance)
    print('Урок создан или изменен')
@receiver(post_delete, sender=Lesson)
def post_delete_lesson(instance,**kwargs):
    update_Product(instance)
    print('Урок удален')




