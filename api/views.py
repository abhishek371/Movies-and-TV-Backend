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


def like(request):
    try:
        movie_id = request.POST['movie_id']
        username = request.POST['username']
    except KeyError:
        raise Http404("Incomplete data")
    if User.objects.filter(pk=username).exists():
        user = User.objects.get(pk=username)
        favorites = user.get_favorites()
        if movie_id in favorites:
            favorites.remove(movie_id)
            response_msg = "Movie removed from favorites"
        else:
            favorites.append(movie_id)
            response_msg = "Movie added to favorites"
        user.favorites = " ".join(favorites)
        user.save()
        return HttpResponse(response_msg)
    else:
        raise Http404("User not present")
