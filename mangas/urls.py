
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search, name="search"),
    path("register", views.register, name="register"),
    path("manga/<str:manga_id>", views.manga, name="manga"),
    path("manga/<str:manga_id>/<str:chapter_id>", views.chapterview, name="chapter"),
    path("add_manga", views.addmanga, name="add_manga"),
    path("rate/<str:manga_id>/<str:num>", views.rate, name="rate"),
    path("searchresponse/<str:q>", views.searchresponse, name="searchresponse"),
    path("addchapter/<str:manga_id>", views.addchapter, name="addchapter"),
    path("addpages/<str:manga_id>/<str:chapter_id>/<str:pagenum>", views.addpages, name="addpages"),
    path("chapteroptions", views.chapteroptions, name="chapteroptions"),
    path("genres", views.genres, name="genres"),
    path("genresearch/<str:genre_id>", views.genresearch, name="genresearch")
 ]