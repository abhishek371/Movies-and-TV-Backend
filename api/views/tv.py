from django.http import JsonResponse
from ..models import TV


def get_all_tv(request):
    tvs = TV.objects.all()
    return JsonResponse(tvs, 200)


def get_tv_details(request, tv_id):
    try:
        tv_details = TV.objects.get(pk=tv_id)
        return JsonResponse(tv_details, 200)
    except TV.DoesNotExist:
        return JsonResponse({"message": "TV with id={} does not exist".format(tv_id)}, 400)
