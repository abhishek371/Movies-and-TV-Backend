import json
import codecs
import requests
from ..models import *
from django.utils.dateparse import parse_date


SEXES = ["O", "F", "M"]


def seed_actors():
    actors_data = codecs.open("api/data/actors.json", encoding="utf_8", errors="ignore").read()
    actors = json.loads(actors_data)["actors"]
    print(actors[3])
    for actor in actors:
        try:
            sex = SEXES[actor["sex"]]
        except KeyError:
            sex = "O"
        Actor(id=actor["id"], name=actor["name"], sex=sex).save()


def seed_directors():
    directors_data = codecs.open("api/data/directors.json", encoding="utf_8", errors="ignore").read()
    directors = json.loads(directors_data)["directors"]
    for director in directors:
        try:
            sex = SEXES[director["sex"]]
        except KeyError:
            sex = "O"
        Director(id=director["id"], name=director["name"], sex=sex).save()


def seed_production_companies():
    prods_data = codecs.open("api/data/production_companies.json", encoding="utf_8", errors="ignore").read()
    prods = json.loads(prods_data)["production_companies"]
    for prod in prods:
        ProductionCompany(id=prod["id"], name=prod["name"]).save()


def seed_genres():
    genres_data = codecs.open("api/data/genres.json", encoding="utf_8", errors="ignore").read()
    genres = json.loads(genres_data)["genres"]
    for genre in genres:
        Genre(id=genre["id"], name=genre["name"]).save()


def seed_movies():
    movies_data = codecs.open("api/data/movies.json", encoding="utf_8", errors="ignore").read()
    movies = json.loads(movies_data)["movies"]
    for movie in movies:
        movie_object = Movie(id=movie["id"], title=movie["title"], runtime=movie["runtime"],
                             release_date=parse_date(movie["release_date"]),
                             ratings=movie["ratings"])
        movie_object.save()
        for genre_id in movie["genres"]:
            genre = Genre.objects.get(pk=genre_id)
            movie_object.genres.add(genre)
        for prod_id in movie["production_companies"]:
            prod = ProductionCompany.objects.get(pk=prod_id)
            movie_object.production_companies.add(prod)
        for actor_id in movie["cast"]:
            actor = Actor.objects.get(pk=actor_id)
            movie_object.cast.add(actor)
        for director_id in movie["directors"]:
            director = Director.objects.get(pk=director_id)
            movie_object.directors.add(director)
        movie_object.save()


def seed_movies_with_plot():
    MOVIE_DETAILS_PRE_URL = "https://api.themoviedb.org/3/movie/"
    MOVIE_DETAILS_SUF_URL = "?api_key=a7d5b9030fe407574db51d1001cb8c90&language=en-US"
    movies = Movie.objects.all()
    movie_collection = []
    print("No of movies: {}".format(len(movies)))
    for index, movie in enumerate(movies):
        print("Movie {}".format(index))
        url = MOVIE_DETAILS_PRE_URL + str(movie.id) + MOVIE_DETAILS_SUF_URL
        movie_details = requests.get(url=url).json()
        attributes_to_remove = ["adult", "backdrop_path", "belongs_to_collection", "budget",
                                "imdb_id", "poster_path", "revenue"]
        for attribute in attributes_to_remove:
            movie_details.pop(attribute, None)
        movie_collection.append(movie_details)
        # movie.plot = movie_details["overview"]
        # movie.save()
    with open("api/data/movie_collection.json", "w") as file:
        json.dump(movie_collection, file, indent=4)


def seed_tv():
    tv_data = codecs.open("api/data/tv.json", encoding="utf_8", errors="ignore").read()
    tvs = json.loads(tv_data)["tv"]
    for tv in tvs:
        tv_object = TV(id=tv["id"], title=tv["title"], ratings=tv["ratings"],
                       start_date=parse_date(tv["start_date"]),
                       no_of_seasons=tv["no_of_seasons"], no_of_episodes=tv["no_of_episodes"])
        tv_object.save()
        for genre_id in tv["genres"]:
            genre = Genre.objects.get(pk=genre_id)
            tv_object.genres.add(genre)
        for prod_id in tv["production_companies"]:
            prod = ProductionCompany.objects.get(pk=prod_id)
            tv_object.production_companies.add(prod)
        for actor_id in tv["cast"]:
            actor = Actor.objects.get(pk=actor_id)
            tv_object.cast.add(actor)
        for director_id in tv["directors"]:
            director = Director.objects.get(pk=director_id)
            tv_object.directors.add(director)
        tv_object.save()


def seed_tv_with_plot():
    TV_DETAILS_PRE_URL = "https://api.themoviedb.org/3/tv/"
    TV_DETAILS_SUF_URL = "?api_key=a7d5b9030fe407574db51d1001cb8c90&language=en-US"
    tvs = TV.objects.all()
    tv_collection = []
    print("No of tvs: {}".format(len(tvs)))
    for index, tv in enumerate(tvs):
        print("Tv {}".format(index))
        url = TV_DETAILS_PRE_URL + str(tv.id) + TV_DETAILS_SUF_URL
        tv_details = requests.get(url=url).json()
        attributes_to_remove = ["backdrop_path", "episode_run_time", "in_production",
                                "poster_path", "status"]
        for attribute in attributes_to_remove:
            tv_details.pop(attribute, None)
        tv_collection.append(tv_details)
        # tv.plot = tv_details["overview"]
        # tv.save()
    with open("api/data/tv_collection.json", "w") as file:
        json.dump(tv_collection, file, indent=4)


def run_seed_with_plot():
    seed_movies_with_plot()
    seed_tv_with_plot()
