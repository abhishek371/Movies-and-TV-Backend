import json
from django.http import HttpResponse, Http404
from ..models import User


def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404("Incomplete data")
    try:
        user = User.objects.get(pk=username)
    except User.DoesNotExist:
        return HttpResponse("Invalid username")
    if user.password != password:
        return HttpResponse("Invalid password")
    return HttpResponse("Successfully logged in")


def signup(request):
    try:
        user_details = json.loads(request.POST['user_details'])
    except KeyError:
        raise Http404("Incomplete data")
    try:
        if User.objects.filter(pk=user_details['username']).exists():
            return HttpResponse("User with username={} already exists".format(user_details['username']))
        User(username=user_details['username'], password=user_details['password'],
             first_name=user_details['first_name'], last_name=user_details['last_name'],
             email=user_details['email'], favorite_movies="", favorite_tv="").save()
        return HttpResponse("Successfully signed up")
    except KeyError:
        raise Http404("Incomplete data")
