from django.http import HttpResponse, Http404
from ..models import User


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
        tv_id = str(request.POST['tv_id'])
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
