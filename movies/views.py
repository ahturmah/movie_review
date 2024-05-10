from django.shortcuts import render, redirect
from movies.models import Movies
from .forms import ReviewForm
from .models import Reviews

#Individual movie page
def movie_page(req, movie_name):
    if req.user.is_authenticated:
        form = ReviewForm(req.POST or None)
        if req.method == "POST":
            form.is_valid()
            formy = form.cleaned_data
            #Creating new review
            obj = Reviews.objects.create(
                reviewer=str(req.user),
                movie_title=movie_name,
                review=formy["review"],
                review_type=formy["review_type"],
            )
            obj.save()
        #Fetching reviews
        reviews = Reviews.objects.filter(movie_title=movie_name)
        #Fetching movie data
        data = Movies.objects.get(title=movie_name)

        form = ReviewForm()
        return render(
            req, "movie.html", context={"movie": data, "form": form, "reviews": reviews}
        )
    else:
        req.session["status"] = 3
        return redirect("login")

#Movies display page
def movies_page(req):
    if req.user.is_authenticated:
        #Fetching movies data
        temp_movies = Movies.objects.all()
        movies = []
        buffy = []
        #Splitting movie data to display in bootstrap grid format
        for index, value in enumerate(temp_movies):
            if (index + 1) % 3 == 0:
                buffy.append(value)
                movies.append(buffy)
                buffy = []
            else:
                buffy.append(value)
            if index == len(temp_movies) - 1 and buffy:
                movies.append(buffy)
        return render(req, "movies.html", context={"movies": movies})
    else:
        req.session["status"] = 3
        return redirect("login")



