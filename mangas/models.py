# Create your models here.
import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os

class User(AbstractUser):
    author = models.BooleanField(default=False)

class Manga(models.Model):
    title = models.CharField(max_length=50)
    ratings = models.ManyToManyField('rating', blank=True, related_name="mangas")
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    genre=models.ManyToManyField('Category', max_length=300)
    cover=models.ImageField( blank = True,
                          null = True,
                          upload_to ='')
    chapters=models.ManyToManyField('chapter',  blank = True, related_name="mangas")
    
    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
        "id":self.id,
        "label": self.title,
        "cover": os.path.basename(self.cover.name)
    }

class Category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.category}"

class Rating(models.Model):
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    manga=models.ForeignKey(Manga, null=True, on_delete=models.CASCADE)
    rating=models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    def __str__(self):
        return f"{self.manga}, {self.user}, {self.rating} stars"

class Image(models.Model):
    manga=models.ForeignKey(Manga, null=True, on_delete=models.CASCADE)
    chapter=models.ForeignKey('chapter', null=True, on_delete=models.CASCADE)
    image=models.ImageField( blank = True,
                          null = True,
                          upload_to ='')
    def __str__(self):
        return f"{self.manga} Chapter {self.chapter.chapter} page"


class Chapter(models.Model):
    chapter=models.IntegerField()
    manga=models.ForeignKey(Manga, null=True, on_delete=models.CASCADE)
    images=models.ManyToManyField(Image, blank=True, related_name="chapters")
    date= models.DateTimeField()
    def __str__(self):
        return f"{self.manga} Chapter {self.chapter}"

    class Meta:
        ordering = ('-date',)
