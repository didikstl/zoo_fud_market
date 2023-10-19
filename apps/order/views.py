from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.order.forms import AddToCartForm, CreateOrderForm
from apps.order.models import Cart, OrderProduct


def get_car_data(user):
    total = 0
    cart = Cart.objects.filter(user=user).select_related('product')
    for row in cart:
        total += row.quantity * row.product.price

    return {'total': total, 'cart': cart}


@login_required  # Декоратор для того, чтобы корзиной могли пользоваться только залогиненные пользователи
def add_to_cart(request):
    data = request.GET.copy()
    data.update(user=request.user)
    request.GET = data

    form = AddToCartForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        crsf = request.session.get('catr_token')  # request.session - это словарь который работает с куки,
        # через него можно добавлять в куки данные.

        if not crsf or crsf != data.get('csrfmiddlewaretoken'):
            row = Cart.objects.filter(user=cd['user'], product=cd['product']).first()
            if row:
                Cart.objects.filter(id=row.id).update(quantity=row.quantity + cd['quantity'])
            else:
                form.save()
            request.session['catr_token'] = data.get('csrfmiddlewaretoken')

        return render(
            request,
            'order/added.html',
            {'product': cd['product'], 'cart': get_car_data(cd['user'])}
        )


@login_required
def cart_view(request):
    cart = get_car_data(request.user)
    breadcrumbs = {'current': 'Корзина'}
    return render(request, 'order/cart.html', {'cart': cart, 'breadcrumbs': breadcrumbs})


@login_required
def create_order_view(request):
    error = None
    user = request.user
    cart = get_car_data(user)
    if not cart['cart']:
        return redirect('index')

    if request.method == 'POST':
        data = request.POST.copy()
        data.update(user=user, total=cart['total'])
        request.POST = data

        form = CreateOrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # менеджер контекста с транзакции,
                    # он автоматически открывается и закрывается после выполнения. Если надо, то можно использовать
                    # декоратор @transaction.atomic перед фукцией.
                    order = form.save()
                    order_products = Cart.objects.filter(user=user).select_related('product')
                    # select_related - выбрать зависимость, при фильтрации по id- user, выбирает еще и товар.
                    # Если его убрать, то все будет работать, но будут лишниие запросы в базу данных.

                    for order_product in order_products:
                        OrderProduct.objects.create(
                            order=order,
                            product=order_product.product,
                            quantity=order_product.quantity,
                            price=order_product.product.price
                        )

                    Cart.objects.filter(user=user).delete()
                    return render(request, 'order/created.html')
            except Exception as e:
                error = f'Заказ не создался. {e}. Напишите, пожалуйста, нашему Менеджеру.'
        else:
            error = form.errors
    else:
        form = CreateOrderForm(data={
            'phone': user.phone if user.phone else '',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
    return render(request, 'order/create.html', {'cart': cart, 'error': error, 'form': form})


@login_required
def delete_from_cart_view(request, product_id):
    Cart.objects.filter(user=request.user, product=product_id).delete()
    return redirect('cart')
