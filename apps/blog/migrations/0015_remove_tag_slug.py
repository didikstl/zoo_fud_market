# Generated by Django 4.2.5 on 2023-09-30 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_rename_tag_tag_name_article_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
    ]
