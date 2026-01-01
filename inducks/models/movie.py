from django.db import models

from inducks.models import helpers


class Movie(models.Model):
    moviecode = models.CharField(max_length=14, primary_key=True)
    title = models.TextField(blank=True, null=True)
    moviecomment = models.TextField(blank=True, null=True)
    appsummary = models.TextField(blank=True, null=True)
    moviejobsummary = models.TextField(blank=True, null=True)
    locked = models.CharField(max_length=1, blank=True, null=True)
    inputfilecode = models.IntegerField(blank=True, null=True)
    maintenanceteamcode = models.CharField(max_length=7, blank=True, null=True)
    appisxapp = models.CharField(max_length=1, blank=True, null=True)
    aka = models.CharField(max_length=81, blank=True, null=True)
    creationdate = models.CharField(max_length=10, blank=True, null=True)
    moviedescription = models.TextField(blank=True, null=True)
    distributor = models.CharField(max_length=50, blank=True, null=True)
    genre = models.CharField(max_length=3, blank=True, null=True)
    orderer = models.CharField(max_length=178, blank=True, null=True)
    publicationdate = models.CharField(max_length=10, blank=True, null=True)
    source = models.CharField(max_length=91, blank=True, null=True)
    tim = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        db_table = 'inducks_movie'


class MovieCharacter(models.Model):
    movie = helpers.InducksForeignKey('Movie', 'characters')
    character = helpers.InducksForeignKey('Character', 'movies')
    istitlecharacter = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_moviecharacter'
        unique_together = ['movie', 'character']


class MovieReference(models.Model):
    story = helpers.InducksForeignKey('Story', 'movie_references')
    movie = helpers.InducksForeignKey('Movie', 'references')
    referencereasonid = models.IntegerField(blank=True, null=True)
    frommovietostory = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_moviereference'
        unique_together = ['story', 'movie']
