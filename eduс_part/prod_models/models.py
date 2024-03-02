from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count
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
    #распределения по группам так, чтобы в каждой группе количество участников не отличалось больше, чем на 1.
    #При этом, минимальные и максимальные значения участников в группе должны быть учтены
    @classmethod
    def create_users(cls):
        # Создание 10 пользователей
        for i in range(1, 11):
            username = f"user_{i}"
            password = f"password{i}"  # Можете использовать разные пароли для каждого пользователя
            email = f"user_{i}@example.com"

            # Создание пользователя
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            print(f"Created user: {username}")
    @classmethod
    def normolize(cls, product):

        groups = Group.objects.filter(
            product=product
            ).annotate(num_users=Count('users'))
        if not groups:
            print("нет группы к продукту:", product.name)
            return -1

        items = []
        # по каждой группе
        for group in groups:
            #print(f"product: {product.name} group: {group.name} {group.num_users}")
            item = {
                    'group_name': group.name,
                    'group_id': group.id,
                    'group_count': group.num_users
                }
            items.append(item)

        total_count = 0
        for item in items:
            total_count += item['group_count']
        group_count = len(items)
        print("Общее количество участников группы:", total_count)
        print("Общее количество групп:", group_count)
        print("Минимальное количество в группе:", product.min_users_per_group)
        print("Максимальное количество в группе:", product.max_users_per_group)
        remainder = total_count % group_count
        division = total_count // group_count
        if total_count > product.max_users_per_group * group_count:
            print("Превышен допустимый предел, добавьте новую группу к продукту:", product.name)
            return -1
        if total_count < product.min_users_per_group:
            print("Слишком мало людей даже для одной группы продукта:", product.name)
            return -1
        abssum = 0
        for item in items:
            item['division'] = division
            if remainder > 0:
                item['required'] = item['division'] + 1
                remainder = remainder - 1
            else:
                item['required'] = item['division']
            item['delta'] = item['group_count'] - item['required']
            abssum = abssum + abs(item['delta'])
        print("items:", items)
        if abssum > 0: #есть необходимость сделать нормализацию
            #print(items)
            #создаем список групп для переброса пользователей
            overages = []
            for item in items:
                if item['delta'] > 0:
                    overage = {
                    'group_id': item['group_id'],
                    'delta': item['delta'],
                        }
                    overages.append(overage)
            print("overages:",overages)
            disadvantages_pool = []
            for item in items:
                if item['delta'] < 0:
                    for i in range(-item['delta']):
                        disadvantage = {
                        'group_id': item['group_id']
                            }
                        disadvantages_pool.append(disadvantage)

            #получаем ID пользователей для переноса
            for overage in overages:
                group_out = Group.objects.get(id=overage['group_id'])
                users = group_out.users.all()[:overage['delta']]

                for idx, user in enumerate(users):
                    group_in = Group.objects.get(id=disadvantages_pool[idx]['group_id'])
                    group_in.users.add(user)
                    if user in group_in.users.all():
                        # Пользователь принадлежит к группе, теперь вы можете выполнить удаление
                        group_out.users.remove(user)
                        print(f"{group_out.name}>>>>>{user.username}>>>>>>{group_in.name}")
                    else:
                        print(f"{group_out.name}>>>>>{user.username}       {group_in.name}")
            #print(disadvantages_pool)
        if total_count < product.min_users_per_group * group_count:
            #необходимо объединить группы
            print("Слишком мало людей для продукта:", product.name)
            return -2
        print(f"******************")
        return 0
    @classmethod
    def join_groups(cls,product):
        groups = Group.objects.filter(
            product=product
            ).annotate(num_users=Count('users'))
        if not groups:
            print("нет группы к продукту:", product.name)
            return -1
        sorted_groups = sorted(groups,
                               key=lambda group: group.num_users, reverse=True)
        items=[]
        for group in sorted_groups:
            item = {
                    'group_name': group.name,
                    'group_id': group.id,
                    'group_count': group.num_users
                }
            items.append(item)
        #print(items)
        total_count = 0
        for item in items:
            total_count += item['group_count']
        group_count = len(items)
        print("Общее количество участников группы:", total_count)
        print("Общее количество групп:", group_count)
        print("Минимальное количество в группе:", product.min_users_per_group)
        print("Максимальное количество в группе:", product.max_users_per_group)
        remainder = total_count % group_count
        division = total_count // group_count
        if total_count < product.min_users_per_group:
            print("недостаточно людей, чтобы собрать группу на продукт:", product.name)
            return -1
        need_group_count = total_count // product.min_users_per_group
        print("Минимальное необходимоее количество групп:", need_group_count)
        need_del_group_count = group_count - need_group_count
        print("Минимальное необходимоее количество групп для удаления:", )
        group_in = sorted_groups[0]
        for group_for_delete in sorted_groups[-need_del_group_count:]:
            users = group_for_delete.users.all()
            print("group_for_delete", group_for_delete.name)
            print("group_in", group_in.name)
            for user in users:
                group_in.users.add(user)
                if user in group_in.users.all():
                    # Пользователь принадлежит к группе, теперь вы можете выполнить удаление
                    group_for_delete.users.remove(user)
                    print(f"{group_for_delete.name}>>>>>{user.username}>>>>>>{group_in.name}")
                else:
                    print(f"{group_for_delete.name}>>>>>{user.username}       {group_in.name}")
            if not group_for_delete.users.count():
                group_for_delete.delete()
                print(f"{group_for_delete.name}>>>>>0")
    @classmethod
    def distribution_groups(cls):
        #получить список продуктов
        products = Product.objects.all()
        for product in products:
            if cls.normolize(product) == -2:
                cls.join_groups(product)
                cls.normolize(product)
        return 0












