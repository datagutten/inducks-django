from django.db import models

from inducks.models import helpers


class InputFile(models.Model):
    inputfilecode = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=11, blank=True, null=True)
    filename = models.CharField(max_length=22, blank=True, null=True)
    layout = models.CharField(max_length=10, blank=True, null=True)
    locked = helpers.InducksBooleanField()
    maintenanceteam = helpers.InducksForeignKey('Team', related_name='files', blank=True, null=True,
                                                db_column='maintenanceteamcode')
    country = helpers.InducksForeignKey('Country', related_name='files', blank=True, null=True)
    language = helpers.InducksForeignKey('Language', related_name='files', blank=True, null=True)
    producercode = models.CharField(max_length=15, blank=True, null=True)
    secundary = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_inputfile'


class Log(models.Model):
    number = models.IntegerField(primary_key=True)
    logkey = models.CharField(max_length=100, blank=True, null=True)
    storycode = models.CharField(max_length=50, blank=True, null=True)
    logid = models.CharField(max_length=4, blank=True, null=True)
    logtype = models.CharField(max_length=1, blank=True, null=True)
    par1 = models.CharField(max_length=1847, blank=True, null=True)
    par2 = models.CharField(max_length=1846, blank=True, null=True)
    par3 = models.CharField(max_length=381, blank=True, null=True)
    marked = helpers.InducksBooleanField()
    inputfilecode = models.IntegerField(blank=True, null=True)
    maintenanceteam = helpers.InducksForeignKey('Team', 'logs', isv_field='maintenanceteamcode', blank=True,
                                                null=True)

    class Meta:
        db_table = 'inducks_log'


class LogData(models.Model):
    logid = models.CharField(max_length=4, primary_key=True)
    category = models.IntegerField(blank=True, null=True)
    logtext = models.CharField(max_length=108, blank=True, null=True)

    class Meta:
        db_table = 'inducks_logdata'
