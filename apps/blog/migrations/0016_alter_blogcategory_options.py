# Generated by Django 4.2.5 on 2023-10-04 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_remove_tag_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'verbose_name': 'Категория блога', 'verbose_name_plural': 'Категория блога'},
        ),
    ]