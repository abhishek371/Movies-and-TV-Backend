from django.http import JsonResponse
from django.core import serializers
from ..models import Movie


def movie_to_dictionary(movie_details):
    movie = {
        "id": movie_details.id,
        "title": movie_details.title,
        "plot": movie_details.plot,
        "release_date": movie_details.release_date,
        "runtime": movie_details.runtime,
        "ratings": movie_details.ratings
        }
    movie["genres"] = []
    for genre in movie_details.genres.all():
        movie["genres"].append({
            "id": genre.id,
            "name": genre.name
        })
    movie["directors"] = []
    for director in movie_details.directors.all():
        movie["directors"].append({
            "id": director.id,
            "name": director.name,
            "sex": director.sex
        })
    movie["cast"] = []
    for actor in movie_details.cast.all():
        movie["cast"].append({
            "id": actor.id,
            "name": actor.name,
            "sex": actor.sex
        })
    movie["production_companies"] = []
    for production_company in movie_details.production_companies.all():
        movie["production_companies"].append({
            "id": production_company.id,
            "name": production_company.name,
        })
    return movie


def get_all_movies(request):
    movies_data = Movie.objects.all()
    movies = []
    for movie_details in movies_data:
        movies.append(movie_to_dictionary(movie_details))
    return JsonResponse({"movies": movies}, status=200)


def get_movie_details(request, movie_id):
    try:
        movie_details = Movie.objects.get(pk=movie_id)
        movie = movie_to_dictionary(movie_details)
        return JsonResponse(movie, status=200)
    except Movie.DoesNotExist:
        return JsonResponse({"message": "Movie with id={} does not exist".format(movie_id)}, status=400)
