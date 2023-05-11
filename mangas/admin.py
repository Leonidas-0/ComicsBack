from django.contrib import admin
from .models import User, Manga, Category, Rating, Chapter, Image, BasicRating


class ChapterAdmin(admin.ModelAdmin):
    list_display=("manga", "chapter")

class MangaAdmin(admin.ModelAdmin):
    filter_horizontal=("chapters", "genre")

class BasicRatingAdmin(admin.ModelAdmin):
    filter_horizontal=("chapters", "genre")


admin.site.register(User)
admin.site.register(BasicRating)
admin.site.register(Manga, MangaAdmin)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Image)
