# Generated by Django 4.2.5 on 2023-09-25 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_tegpost_article_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tegpost',
            options={'verbose_name': 'TAG', 'verbose_name_plural': 'TAGS'},
        ),
    ]
