# Generated by Django 4.2.5 on 2023-09-29 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_tag_options_blogcategory_image_alter_tag_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcategory',
            name='image',
        ),
    ]