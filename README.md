# Small Dependency
Only dependency on this project is pillow for imagefield which can be installed with pip install pillow.

# What is this project?
This project is manga (Asian comics) website, where you can read comics. It is distinct and, in fact, much more complicated than any other cs50 web projects. (1 to 4)


# Have I met all of the the requirements? In my opinion YES!
1. This project is NOT a social network.
2. It is NOT an e-commerce site. NOTE: I made e-commerce site for trading mangas on the other project. This is NOT the website for trading mangas. It is for reading all of mangas AND it is much, much more complex with 6 models in models.py.
3. It utilizes Django (including 6 models) on the back-end and JavaScript on the front-end.
4. My web application is mobile-responsive. Navbar and content changes based on display with.


# Distinctiveness and Complexity

### Structure
Website has 1 app called mangas. In mangas, models.py contains site database. views.py - logic to add, remove, read, rate, search mangas. urls.py contains paths and forms.py contains forms to add manga/chapter/chapter image. Admin.py contains customizations to Django admin page to make sure it is looking pleasent. Javascript file contains "rate manga" functionality of my website. Styles.css is page styling. In manga/images directory manga images are added.

### Models.py
This website is very complex compared to other projects. It utilizes 6 models: User, Manga, Category, Rating, Image and Chapter. Each of mangas has title, ```rating``` (That is manytomany field which points to Rating model. ```Ratings``` object has multiple user values for each Manga. Average value of all ratings for each manga is then calculated in views.py), ```author``` (which is user. NOTE: Not all users are authors. It is determined during registration where you are asked whether you are author or not), ```genre``` (It is manytomanyfield which points to category. Basically genre of the manga), ```Cover``` (front image of manga) and ```chapters``` (Each manga has multiple chapters so it is also manytomany field). ```Chapters``` model has manytomanyfield of images. Each manga has multiple chapters. Each chapter has multiple images. ```Image``` model has foreignkeys manga, chapter and of course image. ```Rating``` model has foreignkey user, manga, and rating. ```Category``` has only one field: category.

### templates views and urls
Path:```""``` is page's index. It displays all of mangas with all the fields (including latest uploaded chapter) in Manga model. In index view I calculate average rating (from manytomany object called rating), join it with manga and paginate the result. 

Path: ```search``` makes up the functionality of search bar in my website. In searchbox, if you type exact name of manga, you are redirected right to that manga page. If there are multiple results with that search keyward, you are redirected on result page with similar content to index, but search results insted of it. If keyward is only 1 letter or matches no manga, you are redirected to "no result" page.

Path: ```manga/<str:manga_id>``` redirects to manga page. All of paginated chapters are displayed there. You can click on any chapters to view corresponding chapter content. You can also rate manga, just as you could in main page.

Path ```manga/<str:manga_id>/<str:chapter_id>``` redirects to chapter page where images are displayed and where you can actually read manga. There also are next, previous chapter navigation buttons.

Path ```add_manga``` redirects to page for adding mangas if you are an author of course. 

Template at path ```addchapter/<str:manga_id>``` adds chapter for manga with specific id.

Template at path ```addpages/<str:manga_id>/<str:chapter_id>/<str:pagenum>``` adds images for select manga chapter. You can select how many images to add. This number is then looped in views.py and adds corresponding number of images.

Template at path ```genres``` lists all genres. When clicked on genre, you are redirected to```genresearch/<str:genre_id>```which lists all mangas for chosen category.

There are also register, login and logout urls.

### JavaScript implementation
My website uses JavaScript to display search results dynamically. When typing keyward url is fetched with path ```searchresponse/<str:q>``` in which ```q``` represents search keyward. Then if q matches with result(s), latter are sent to template as JSON objects. Then I create corresponding links with paths related to appropriate results in JS.

Second functionallity of Javascript is rate in which same process as above is repeated. Rating is sent to view. Then that rating is added to model and average is calculated once more. Then response is sent back to template. NOTE: if rating of a particullar user is already present, new rating is not added.

# Thanks
I hope I pass this evaluation. Thank you for this amazing course. And your hard work. :)

