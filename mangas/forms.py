from .models import Category, Manga, Image, Chapter
from django import forms
from django.forms import ModelForm

class MangaForm(ModelForm):
    genres = forms.ModelMultipleChoiceField(
    label='Genre(s)',
    queryset=Category.objects.all(),
    widget=forms.CheckboxSelectMultiple()
    )
    class Meta:
        model = Manga
        fields = ["title", "description", "cover", "genres"]



class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ["chapter"]
        widgets = {
        }

class ImageForm(ModelForm):
    class Meta:
        model=Image
        fields=["image"]
