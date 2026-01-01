from django.db import models

from inducks.models import helpers


class Publication(models.Model):
    publicationcode = models.CharField(max_length=12, primary_key=True)
    country = helpers.InducksForeignKey('Country', related_name='publications')
    language = helpers.InducksForeignKey('Language', related_name='publications')
    title = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=82, blank=True, null=True)
    publicationcomment = models.TextField(blank=True, null=True)
    circulation = models.CharField(max_length=15, blank=True, null=True)
    numbersarefake = helpers.InducksBooleanField()
    error = helpers.InducksBooleanField()
    locked = helpers.InducksBooleanField()
    inxforbidden = helpers.InducksBooleanField()
    inputfilecode = models.IntegerField(blank=True, null=True)
    maintenanceteamcode = models.CharField(max_length=9, blank=True, null=True)

    # maintenanceteam = helpers.InducksForeignKey('Main')

    class Meta:
        db_table = 'inducks_publication'


class PublicationCategory(models.Model):
    publication = helpers.InducksForeignKey('Publication', 'categories')
    category = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'inducks_publicationcategory'
        unique_together = ['publication', 'category']

    def __str__(self):
        return self.category


class PublicationName(models.Model):
    publication = helpers.InducksForeignKey('Publication', 'names')
    publicationname = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'inducks_publicationname'
        unique_together = ['publication', 'publicationname']

    def __str__(self):
        return self.publicationname


class Publisher(models.Model):
    publisherid = models.CharField(max_length=100, primary_key=True)
    publishername = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_publisher'

    def __str__(self):
        return self.publishername
