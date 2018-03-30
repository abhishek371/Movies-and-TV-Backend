from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    password = models.CharField(max_length=1000)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    favorites = models.CharField(max_length=1000000000, blank=True)

    def get_favorites(self):
        return list(map(str, self.favorites.split()))

    def get_favorites_as_string(self):
        if self.get_favorites():
            return '["' + '", "'.join(self.get_favorites()) + '"]'
        else:
            return "[]"

    def __str__(self):
        return '{"username": "' + self.username + '", "first_name": "' + self.first_name + '", "last_name": "' + \
               self.last_name + '", "email": "' + self.email + '", "favorites": ' + self.get_favorites_as_string()+' }'
