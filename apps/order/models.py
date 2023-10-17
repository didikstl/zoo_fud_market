from django.db import models

from apps.catalog.models import Product
from apps.user.models import User
from phonenumber_field.modelfields import PhoneNumberField



class Cart(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name='Итого', max_digits=12, decimal_places=2)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    email = models.EmailField(verbose_name='E-mail')
    phone = PhoneNumberField(verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес')
    comment = models.TextField(verbose_name='Коментарий', null=True, blank=True)
    created_ad = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_ad = models.DateTimeField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'