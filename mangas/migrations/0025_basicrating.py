# Generated by Django 4.0.6 on 2023-05-08 10:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mangas', '0024_remove_user_coins_image_chapter_alter_chapter_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('manga', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mangas.manga')),
            ],
        ),
    ]
