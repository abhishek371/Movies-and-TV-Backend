from django.http import JsonResponse
from django.core import serializers
from ..models import TV


def get_all_tv(request):
    tvs = TV.objects.all()
    tvs_serialized = serializers.serialize('json', tvs)
    return JsonResponse(tvs_serialized, status=200, safe=False)


def get_tv_details(request, tv_id):
    try:
        tv_details = TV.objects.get(pk=tv_id)
        tv = {
            "id": tv_details.id,
            "title": tv_details.title,
            "plot": tv_details.plot,
            "start_date": tv_details.start_date,
            "ratings": tv_details.ratings,
            "no_of_seasons": tv_details.no_of_seasons,
            "no_of_episodes": tv_details.no_of_episodes
        }
        tv["genres"] = []
        for genre in tv_details.genres.all():
            tv["genres"].append({
                "id": genre.id,
                "name": genre.name
            })
        tv["directors"] = []
        for director in tv_details.directors.all():
            tv["directors"].append({
                "id": director.id,
                "name": director.name,
                "sex": director.sex
            })
        tv["cast"] = []
        for actor in tv_details.cast.all():
            tv["cast"].append({
                "id": actor.id,
                "name": actor.name,
                "sex": actor.sex
            })
        tv["production_companies"] = []
        for production_company in tv_details.production_companies.all():
            tv["production_companies"].append({
                "id": production_company.id,
                "name": production_company.name,
            })
        return JsonResponse(tv, status=200)
    except TV.DoesNotExist:
        return JsonResponse({"message": "TV with id={} does not exist".format(tv_id)}, status=400)
