from django.db import models
from inducks.models import helpers


class Person(models.Model):
    personcode = models.CharField(max_length=79, primary_key=True)
    nationality = helpers.InducksForeignKey('Country', related_name='persons',
                                            db_column='nationalitycountrycode',
                                            isv_field='nationalitycountrycode', blank=True, null=True)
    fullname = models.TextField(blank=True, null=True)
    official = helpers.InducksBooleanField()
    personcomment = models.CharField(max_length=221, blank=True, null=True)
    unknownstudiomember = helpers.InducksBooleanField()
    isfake = helpers.InducksBooleanField()
    numberofindexedissues = models.IntegerField(blank=True, null=True)
    birthname = models.TextField(blank=True, null=True)
    borndate = helpers.InducksDateField(max_length=10, blank=True, null=True)
    bornplace = models.CharField(max_length=30, blank=True, null=True)
    deceaseddate = helpers.InducksDateField(blank=True, null=True)
    deceasedplace = models.CharField(max_length=31, blank=True, null=True)
    education = models.CharField(max_length=189, blank=True, null=True)
    moviestext = models.CharField(max_length=879, blank=True, null=True)
    comicstext = models.CharField(max_length=927, blank=True, null=True)
    othertext = models.CharField(max_length=307, blank=True, null=True)
    photofilename = models.CharField(max_length=32, blank=True, null=True)
    photocomment = models.CharField(max_length=68, blank=True, null=True)
    photosource = models.CharField(max_length=67, blank=True, null=True)
    personrefs = models.CharField(max_length=179, blank=True, null=True)

    class Meta:
        db_table = 'inducks_person'

    @property
    def image_url(self):
        return 'https://inducks.org/creators/photos/%s' % self.photofilename

    def __str__(self):
        return self.fullname


class PersonAlias(models.Model):
    person = helpers.InducksForeignKey('Person', related_name='aliases')
    surname = models.CharField(max_length=48, blank=True, null=True)
    givenname = models.CharField(max_length=31, blank=True, null=True)
    official = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_personalias'
        unique_together = ['person', 'surname', 'givenname']
