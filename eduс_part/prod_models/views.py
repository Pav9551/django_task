from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, UserProduct, Group
# Create your views here.

# Функция для перераспределения пользователей в группы
def redistribute_groups(product):
    # Получаем всех пользователей, которые имеют доступ к продукту
    user_products = UserProduct.objects.filter(product=product)
    users_count = user_products.count()

    # Получаем текущие группы продукта
    groups = Group.objects.filter(product__id=product.id)

    # Распределяем пользователей по группам
    for i, user_product in enumerate(user_products):
        # Выбираем группу для пользователя
        group_index = i % groups.count()
        group = groups[group_index]

        # Добавляем пользователя в выбранную группу
        group.users.add(user_product.user)

def main_view(request):
    products = Product.objects.all()
    return render(request, 'prod_models_app/index.html', context={'products': products})
def empty_view(request):
    products = Product.objects.all()
    return render(request, 'prod_models_app/empty.html', context={'products': products})
def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'prod_models_app/product.html', context={'product': product})
def user_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        if Group.find_product_groups(product) > 0:
            print('найдена группа(ы) соответствующая данному продукту')
            if Group.find_user_in_groups(product) > 0:
                print('пользователь уже связан с продуктом - это метка, что он уже есть в группе')
            else:
                print('пользователь еще не связан с продуктом')
                if Group.find_user(product) > 0:
                    print('пользователь уже принадлежит одной из групп, но не связан с продуктом!!!')
                else:
                    print('пользователь еще не принадлежит ни одной группе')
                    if Group.find_free_running_group(product) > 0:
                        print('распределено в наиболее занятую запущенную группу')
                    else:
                        if Group.find_free_onhold_group(product) > 0:
                            print('распределено в наименее занятую и не запущенную группу')
                        else:
                            print('Нет мест в группах')
        else:
            print('группы не найдены')
        return redirect('/')
    else:
        return render(request, 'prod_models_app/product.html', context={'product': product})
