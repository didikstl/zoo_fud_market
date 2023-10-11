from django.db import models
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField, ImageSpecField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from pilkit.processors import ResizeToFill

from apps.main.mixins import MetaTagMixin
from config.settings import MEDIA_ROOT


class Category(MPTTModel, MetaTagMixin):
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

    def get_absolute_url(self):
        return reverse('categories', args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ProductImage(models.Model):
    image = ProcessedImageField(
        verbose_name='Изображение',
        upload_to='catalog/product/',

    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 400)]
    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name='Основное изображение', default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Функция для выставления приоритетного изображения в админке
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        if self.is_main:
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return ''

    def image_tag_thumbnail(self):
        """
        Функция добавление миниатюры изображения
        :return:
        """
        if not self.image_thumbnail:
            ProductImage.objects.get(id=self.id)
        return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image_thumbnail}' width='70'>")

    image_tag_thumbnail.short_description = 'Текущее изображение'

    def image_tag(self):
        if not self.image_thumbnail:
            ProductImage.objects.get(id=self.id)
        return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image_thumbnail}'>")

    image_tag.short_description = 'Текущее изображение'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


class Product(MetaTagMixin):
    name = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(unique=True, verbose_name='Слаг (Алиас, ЧПУ)')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2, default=0)
    categories = models.ManyToManyField(Category, verbose_name='Категории', through='ProductCategory', blank=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def images(self):
        return ProductImage.objects.filter(product=self.id)

    def main_image(self):
        image = ProductImage.objects.filter(product=self.id, is_main=True).first()
        if not image:
            image = self.images().first()
        return image

    def image_tag(self):
        image = self.main_image()
        if image:
            return image.image_tag_thumbnail()

    def __str__(self):  # Возвращает название товара в виде строки.
        return self.name

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    is_main = models.BooleanField(verbose_name='Основная категория', default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_main:
            ProductCategory.objects.filter(product=self.product).update(is_main=False)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'
