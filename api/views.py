import json
from django.http import HttpResponse, Http404
from .models import User


def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404("Incomplete data")
    try:
        user = User.objects.get(pk=username)
    except User.DoesNotExist:
        raise Http404("Invalid username")
    if user.password != password:
        raise Http404("Invalid password")
    return HttpResponse("Successfully logged in")


def signup(request):
    try:
        user_details = json.loads(request.POST['user_details'])
    except KeyError:
        raise Http404("Incomplete data")
    try:
        if User.objects.filter(pk=user_details['username']).exists():
            raise Http404("User with username={} already exists".format(user_details['username']))
        User(username=user_details['username'], password=user_details['password'], first_name=user_details['first_name'],
             last_name=user_details['last_name'], email=user_details['email'], favorites="").save()
        return HttpResponse("Successfully signed up")
    except KeyError:
        raise Http404("Incomplete data")


def get_user_details(request, username):
    if User.objects.filter(pk=username).exists():
        return HttpResponse(User.objects.get(pk=username))
    return Http404("User not found")


def like_movie(request):
    try:
        movie_id = str(request.POST['movie_id'])
        username = request.POST['username']
    except KeyError:
        raise Http404("Incomplete data")
    if User.objects.filter(pk=username).exists():
        user = User.objects.get(pk=username)
        favorites = user.get_favorite_movies()
        if movie_id in favorites:
            favorites.remove(movie_id)
            response_msg = "Movie removed from favorites"
        else:
            favorites.append(movie_id)
            response_msg = "Movie added to favorites"
        user.favorite_movies = " ".join(favorites)
        user.save()
        return HttpResponse(response_msg)
    else:
        raise Http404("User not present")


def like_tv(request):
    try:
        tv_id = str(request.POST['movie_id'])
        username = request.POST['username']
    except KeyError:
        raise Http404("Incomplete data")
    if User.objects.filter(pk=username).exists():
        user = User.objects.get(pk=username)
        favorites = user.get_favorite_tv()
        if tv_id in favorites:
            favorites.remove(tv_id)
            response_msg = "TV removed from favorites"
        else:
            favorites.append(tv_id)
            response_msg = "TV added to favorites"
        user.favorite_tv = " ".join(favorites)
        user.save()
        return HttpResponse(response_msg)
    else:
        raise Http404("User not present")
