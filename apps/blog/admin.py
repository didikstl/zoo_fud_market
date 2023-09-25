from django.contrib import admin
from apps.blog.models import BlogCategory, Article, Teg


admin.site.register(BlogCategory)
admin.site.register(Article)
admin.site.register(Teg)
