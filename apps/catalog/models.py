from django.db import models
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from pilkit.processors import ResizeToFill

from config.settings import MEDIA_ROOT


class Category(MPTTModel):
    name = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(unique=True, verbose_name='Слаг (Алиас, ЧПУ)')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    image = ProcessedImageField(
        verbose_name='Изображение',
        upload_to='catalog/category/',
        processors=[ResizeToFill(600, 400)],
        null=True,
        blank=True
    )
    parent = TreeForeignKey(
        to='self',
        verbose_name='Родитель',
        related_name='child',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f'<img src="/{MEDIA_ROOT}{self.image}" width="70">')

    image_tag_thumbnail.short_description = 'Изображение'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="/{MEDIA_ROOT}{self.image}">')

    image_tag.short_description = 'Изображение'

    def __str__(self):
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return ' ->'.join(full_path[::-1])


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(unique=True, verbose_name='Слаг (Алиас, ЧПУ)')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self): # Возвращает название товара в виде строки.
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

