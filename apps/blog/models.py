from django.db import models


class BlogCategory(models.Model):
    name = models.CharField(verbose_name='Имя категории', max_length=255)

    def __str__(self):
        """
        функция для того, чтобы в админке сайта написались категории с названиеми, которые мы сами написали
        :return:
        """
        return self.name

    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'


class Article(models.Model):
    """
    Article - статьи,

    """
    category = models.ForeignKey(to=BlogCategory, verbose_name='Категория',  on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    text_preview = models.TextField(verbose_name="Текс-превью", null=True, blank=True)  # может быть пустым
    text = models.TextField(verbose_name="Текс")
    publish_date = models.DateTimeField(verbose_name='Дата публикации')
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)  # Дата будет писаться автоматически
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True) # Создастся один раз
    tags = models.ManyToManyField('Teg', blank=True, related_name='tags')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Teg(models.Model):
    tag = models.CharField(verbose_name='TAG', max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag


    class Meta:
        verbose_name = 'TAG'
        verbose_name_plural = 'TAGS'





