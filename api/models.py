from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    password = models.CharField(max_length=1000)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    favorite_movies = models.CharField(max_length=1000000000, blank=True)
    favorite_tv = models.CharField(max_length=1000000000, blank=True)

    def get_favorite_movies(self):
        return list(map(str, self.favorite_movies.split()))

    def get_favorite_tv(self):
        return list(map(str, self.favorite_tv.split()))

    def get_favorite_movies_as_string(self):
        if self.get_favorite_movies():
            return '["' + '", "'.join(self.get_favorite_movies()) + '"]'
        else:
            return "[]"

    def get_favorite_tv_as_string(self):
        if self.get_favorite_tv():
            return '["' + '", "'.join(self.get_favorite_tv()) + '"]'
        else:
            return "[]"

    def __str__(self):
        return '{"username": "' + self.username + '", "first_name": "' + self.first_name + '", "last_name": "' + \
               self.last_name + '", "email": "' + self.email + '", "favorite_movies": ' + \
               self.get_favorite_movies_as_string() + ', "favorite_tv": ' + self.get_favorite_tv_as_string() + ' }'
