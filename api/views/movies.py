from django.http import JsonResponse
from ..models import Movie


def get_all_movies(request):
    movies = Movie.objects.all()
    return JsonResponse(movies, 200)


def get_movie_details(request, movie_id):
    try:
        movie_details = Movie.objects.get(pk=movie_id)
        return JsonResponse(movie_details, 200)
    except Movie.DoesNotExist:
        return JsonResponse({"message": "Movie with id={} does not exist".format(movie_id)}, 400)
