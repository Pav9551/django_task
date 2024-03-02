from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_users_per_group = models.PositiveIntegerField()
    max_users_per_group = models.PositiveIntegerField()
    lessoncount = models.PositiveIntegerField(blank=True, null=True)
    def __str__(self):
        return f' {self.name}'

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_lessons')
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ManyToManyField(User,blank=True, related_name='educ_groups')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
    @classmethod
    def get_user(cls):
        # Получаем модель пользователя
        UserModel = get_user_model()
        # Получаем имя поля, используемое как имя пользователя
        username_field = UserModel.USERNAME_FIELD
        user = UserModel.objects.get(pk=1)  # Получение пользователя
        username = getattr(user, username_field)
        print(username)
        return user

    @classmethod
    def find_product_groups(cls, product):
        # Теперь найдем все группы, связанные с этим продуктом
        groups_with_product = Group.objects.filter(product=product)
        for group in groups_with_product:
            print(group.name)
        return groups_with_product.count()

    @classmethod
    def find_user_in_groups(cls, product):
        user = Group.get_user()
        # Подсчет числа групп, к которым относится пользователь и которые соответствуют продукту
        number_of_groups_for_user_and_product = Group.objects.filter(
            product__user_products__user=user,
            product=product
        ).count()
        return number_of_groups_for_user_and_product
    @classmethod
    def find_user(cls, product):
        user = Group.get_user()
        # Подсчет числа групп, к которым относится пользователь и которые соответствуют продукту
        number_of_groups_for_user = Group.objects.filter(
            users=user,
            product=product
        ).count()
        return number_of_groups_for_user
    @classmethod
    def find_free_running_group(cls, product):
        user = Group.get_user()
        # Получение числа групп, которые соответствуют продукту и запушены
        started_groups = Group.objects.filter(
            product__start_date__lte=timezone.now(),
            product=product
        )
        # Сортировка групп по количеству свободных мест (в порядке возрастания)
        sorted_groups = sorted(started_groups, key=lambda group: product.max_users_per_group - group.users.count())
        '''for group in sorted_groups:
            # Получаем количество пользователей, добавленных в эту группу
            users_count = group.users.count()
            # Определяем количество свободных мест
            free_slots = product.max_users_per_group - users_count
            # Выводим информацию о группе и количестве свободных мест
            print(f"Группа запущена: {group.name}, Свободные места: {free_slots}")'''
        group_with_most_free_slots = sorted_groups[0] if sorted_groups else False
        free_slots = 0
        #необходимо убедиться, что есть свободные места в найденной группе, т.к в процессе поиска их могли занять
        if group_with_most_free_slots:
            free_slots = product.max_users_per_group - group_with_most_free_slots.users.count()
        if free_slots > 0:
            print(f"Добавляем в группу {group_with_most_free_slots.name}")
            group_with_most_free_slots.users.add(user)
            print(f"Создаем запись о добавлении")
            new_user_product = UserProduct(user=user, product=product)
            new_user_product.save()

        else:
            print(f"Нет мест в запущенной группе")
        return free_slots
    @classmethod
    def find_free_onhold_group(cls, product):
        user = Group.get_user()
        # Получение числа групп, которые соответствуют продукту и не запушены
        started_groups = Group.objects.filter(
            product__start_date__gte=timezone.now(),
            product=product
        )
        # Сортировка групп по количеству свободных мест (в порядке убывания)
        sorted_groups = sorted(started_groups,
                               key=lambda group: product.max_users_per_group - group.users.count(), reverse=True)
        '''for group in sorted_groups:
            # Получаем количество пользователей, добавленных в эту группу
            users_count = group.users.count()
            # Определяем количество свободных мест
            free_slots = product.max_users_per_group - users_count
            # Выводим информацию о группе и количестве свободных мест
            print(f"Группа еще не запущена: {group.name}, Свободные места: {free_slots}")'''
        group_with_most_free_slots = sorted_groups[0] if sorted_groups else False
        free_slots = 0
        #необходимо убедиться, что есть свободные места в найденной группе, т.к в процессе поиска их могли занять
        if group_with_most_free_slots:
            free_slots = product.max_users_per_group - group_with_most_free_slots.users.count()
        if free_slots > 0:
            print(f"Добавляем в группу {group_with_most_free_slots.name}")
            group_with_most_free_slots.users.add(user)
            print(f"Создаем запись о добавлении")
            new_user_product = UserProduct(user=user, product=product)
            new_user_product.save()
        else:
            print(f"Нет мест в не запущенной группе")
        return free_slots








