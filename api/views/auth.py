import json
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from ..models import User


def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(pk=username)
    except KeyError:
        return JsonResponse({"message": "Incomplete data"}, 400)
    except User.DoesNotExist:
        return JsonResponse({"message": "Invalid username"}, 400)
    if user.password != password:
        return JsonResponse({"message": "Invalid password"}, 400)
    return JsonResponse({"message": "Successfully logged in"}, 200)


def signup(request):
    try:
        user_details = json.loads(request.POST['user_details'])
        if User.objects.filter(pk=user_details['username']).exists():
            return JsonResponse({"message": "User with username={} already exists".
                                            format(user_details['username'])}, 400)
        User(username=user_details['username'], password=user_details['password'],
             name=user_details['name'], email=user_details['email'],
             dob=parse_date(user_details["dob"]), sex=user_details["sex"]).save()
        return JsonResponse({"message": "Successfully signed up"}, 200)
    except KeyError:
        return JsonResponse({"message": "Incomplete data"}, 400)
