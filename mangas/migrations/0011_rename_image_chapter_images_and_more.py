# Generated by Django 4.0.3 on 2022-04-07 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangas', '0010_alter_chapter_chapter_alter_manga_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='image',
            new_name='images',
        ),
        migrations.RenameField(
            model_name='manga',
            old_name='rating',
            new_name='ratings',
        ),
    ]
