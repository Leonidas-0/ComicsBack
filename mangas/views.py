from json import JSONDecodeError
import re
from django.shortcuts import render
from urllib.request import Request
from django.contrib.auth import authenticate, login, logout
from .models import User, Manga, Category, Chapter, Rating, Image, BasicRating
from .forms import MangaForm, ChapterForm, ImageForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Avg
from django.db.models import Max
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    mangas = Manga.objects.annotate(recent_date=Max(
        'chapters__date')).order_by('-recent_date')
    ratings = []
    for i in mangas:
        ratingdict = i.ratings.aggregate(Avg('rating'))
        rating = ratingdict.get('rating__avg')
        if rating == None:
            rating = 0
        ratings.append(rating)
    # zippedList = zip(mangas, ratings)
    # paginated = paginate(request, list(zippedList), 8)
    return(JsonResponse([l.serialize() for l in Manga.objects.all()], safe=False))
    # return render(request, "mangas/index.html", {"mangas": paginated, })


def paginate(request, titles, num):
    paginator = Paginator(titles, num)
    page_number = request.GET.get('page')
    paginated = paginator.get_page(page_number)
    return paginated


@login_required(login_url='http://127.0.0.1:8000/login')
def search(request):
    q = request.GET.get('q')
    if len(q) == 1 or q == "":
        return render(request, "mangas/notfound.html")
    mangas = [i for i in Manga.objects.all() if q.lower() == i.title.lower()]
    if len(mangas) == 1:
        q = mangas[0]
        return HttpResponseRedirect("manga/"+str(Manga.objects.get(title=q).id))
    else:
        resultlist = []
        ratings = []
        resultlist = [i for i in Manga.objects.all() if q.lower() in i.title.lower()]
        for i in Manga.objects.all():
            ratingdict = i.ratings.aggregate(Avg('rating'))
            rating = ratingdict.get('rating__avg')
            if rating == None:
                rating = 0
            ratings.append(rating)
        zippedList = zip(resultlist, ratings)
        return render(request, "mangas/results.html", {
            "mangas": zippedList,
            "q": q,
        })
        return render(request, "mangas/notfound.html")


@login_required(login_url='http://127.0.0.1:8000/login')
def genres(request):
    genres = Category.objects.all()
    return render(request, "mangas/genres.html", {"genres": genres})


@login_required(login_url='http://127.0.0.1:8000/login')
def genresearch(request, genre_id):
    mangas = Manga.objects.filter(genre__id__in=[genre_id]).annotate(
        recent_date=Max('chapters__date')).order_by('-recent_date')
    genre = Category.objects.get(id=genre_id)
    ratings = []
    for i in mangas:
        ratingdict = i.ratings.aggregate(Avg('rating'))
        rating = ratingdict.get('rating__avg')
        if rating == None:
            rating = 0
        ratings.append(rating)
    zippedList = zip(mangas, ratings)
    return render(request, "mangas/genresearch.html", {"mangas": zippedList, "genre": genre, "length": len(Manga.objects.all())})


@login_required(login_url='http://127.0.0.1:8000/login')
def addchapter(request, manga_id):
    if not request.user.author:
        return redirect('index')
    manga = Manga.objects.get(id=manga_id)
    try:
        lastadded = list(Chapter.objects.filter(mangas__id=manga_id))[0]
    except IndexError:
        lastadded = None
    newchapter = ChapterForm(request.POST or None, request.FILES or None)
    pagenum = ""
    if newchapter.is_valid():
        pagelength = request.POST.get("pagelength")
        for i in range(int(pagelength)):
            pagenum += "a"
            i += 1
        savechapter = newchapter.save(commit=False)
        savechapter.author = request.user
        savechapter.manga = manga
        savechapter.date = datetime.today()
        savechapter.save()
        manga.chapters.add(savechapter)
        return redirect("addpages", manga_id, savechapter.id, pagenum)
    return render(request, "mangas/addchapter.html", {"chapterform": newchapter, "lastadded": lastadded, "manga": manga})


@login_required(login_url='http://127.0.0.1:8000/login')
def addpages(request, manga_id, chapter_id, pagenum):
    if not request.user.author:
        return redirect('index')
    manga = Manga.objects.get(id=manga_id)
    newimage = ImageForm(request.POST or None, request.FILES or None)
    chapter = Chapter.objects.filter(manga=manga).get(id=chapter_id)
    if request.method == "POST":
        if manga.author == request.user:
            i = 1
            while(i < len(pagenum)):
                try:
                    newimage = Image.objects.create(
                        manga=manga, chapter=chapter, image=request.FILES["image"+str(i)])
                    chapter.images.add(newimage)
                    i += 1
                except:
                    return redirect("index")
    return render(request, "mangas/addpages.html", {"pageform": newimage, "pagenum": pagenum})


@login_required(login_url='http://127.0.0.1:8000/login')
def addmanga(request):
    if not request.user.author:
        return redirect('index')
    newmanga = MangaForm(request.POST or None, request.FILES or None)
    if request.user.author == True:
        if newmanga.is_valid():
            savemanga = newmanga.save(commit=False)
            savemanga.author = request.user
            genre = newmanga.cleaned_data['genres']
            savemanga.save()
            for i in genre:
                savemanga.genre.add(i)
            return redirect("addchapter", savemanga.id)
    return render(request, "mangas/addmanga.html", {"mangaform": newmanga})


# @login_required(login_url='http://127.0.0.1:8000/login')
def manga(request, manga_id):
    manga = Manga.objects.get(id=manga_id)
    ratingdict = manga.ratings.aggregate(Avg('rating'))
    rating = ratingdict.get('rating__avg')
    if rating == None:
        rating = 0
    chapters = Chapter.objects.filter(manga__in=[manga])
    paginated = paginate(request, list(chapters), 100)
    return(JsonResponse(manga.serialize(),  safe=False))
    # return render(request, "mangas/manga.html", {"chapters": paginated, "manga": manga, "rating": rating})


# @login_required(login_url='http://127.0.0.1:8000/login')
def rate(request, manga_id, num):
    newrating = BasicRating.objects.create(manga=Manga.objects.get(id=manga_id), rating=int(num))
    Manga.objects.get(id=manga_id).basicRating.add(newrating)
    return(JsonResponse(("ok"), safe=False))
    # if request.method == "POST":
    #     rated = Manga.objects.filter(id=manga_id).filter(
    #         ratings__user__in=[request.user])
    #     if not rated:
    #         newrating = Rating.objects.create(manga=Manga.objects.get(
    #             id=manga_id), user=request.user, rating=int(num) + 1)
    #         Manga.objects.get(id=manga_id).ratings.add(newrating)
    #         return(JsonResponse([num], safe=False))
    #     else:
    #         return(JsonResponse("Rated previously!", safe=False))


@login_required(login_url='http://127.0.0.1:8000/login')
def chapteroptions(request):
    mangas = Manga.objects.filter(author=request.user)
    return render(request, "mangas/chapteroptions.html", {"mangas": mangas})


@login_required(login_url='http://127.0.0.1:8000/login')
def chapterview(request, manga_id, chapter_id):
    manga = Manga.objects.get(id=manga_id)
    chapter = Chapter.objects.filter(manga__in=[manga]).get(id=chapter_id)
    pages = chapter.images.all()
    mangachapters = list(Chapter.objects.filter(mangas__id=manga_id))[::-1]
    count = 0
    for i in mangachapters:
        count += 1
        if i == chapter:
            try:
                nextchapter = mangachapters[count]
            except IndexError:
                nextchapter = None
            try:
                if count-2 != -1:
                    prevchapter = mangachapters[count-2]
                else:
                    prevchapter = None
            except IndexError:
                prevchapter = None
            break
    return render(request, "mangas/pages.html", {"chapter": chapter, "nextchapter": nextchapter, "prevchapter": prevchapter, "manga": manga, "pages": pages})


def searchresponse(request, q):
    resultlist = [i.serialize() for i in Manga.objects.all()
        if q.lower() in i.title.lower()]
    if resultlist:
        if len(q) > 1:
            return(JsonResponse(resultlist, safe=False))
        else: return JsonResponse("", safe=False)
    else:
        return JsonResponse("", safe=False)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mangas/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mangas/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mangas/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            if "Yes" in request.POST:
                user.author = True
            else:
                user.author = False
            user.save()
        except IntegrityError:
            return render(request, "mangas/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mangas/register.html")
