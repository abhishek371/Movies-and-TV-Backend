from django.db import models
from datetime import date


class Director(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    dob = models.DateField()
    sex = models.CharField(max_length=1)


class Genre(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)


class ProductionCompany(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=40)
    homepage_link = models.CharField(max_length=100)
    origin_country = models.CharField(max_length=20)


class Actor(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    dob = models.DateField()
    sex = models.CharField(max_length=1)


class Movies(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    release_date = models.DateField()
    runtime = models.IntegerField()
    ratings = models.FloatField()
    production_company = models.ForeignKey(ProductionCompany, on_delete=models.CASCADE)
    directors = models.ManyToManyField(Director)
    cast = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)


class TV(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    ratings = models.FloatField()
    no_of_seasons = models.IntegerField()
    no_of_episodes = models.IntegerField()
    cast = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)
    genres = models.ManyToManyField(Genre)
    production_companies = models.ManyToManyField(ProductionCompany)


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    password = models.CharField(max_length=1000)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    dob = models.DateField(default=date.today)
    sex = models.CharField(max_length=1)
    liked_movies = models.ManyToManyField(Movies)
    liked_tv = models.ManyToManyField(TV)
