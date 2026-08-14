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
    logid = helpers.InducksForeignKey('LogData')
    logtype = models.CharField(max_length=1, blank=True, null=True)
    par1 = models.TextField(blank=True, null=True)
    par2 = models.TextField(blank=True, null=True)
    par3 = models.TextField(blank=True, null=True)
    marked = helpers.InducksBooleanField()
    inputfile = helpers.InducksForeignKey('InputFile', blank=True, null=True)
    maintenanceteam = helpers.InducksForeignKey('Team', 'logs', isv_field='maintenanceteamcode', blank=True,
                                                null=True)

    def __str__(self):
        if self.logid:
            text = self.logid.logtext
            count = sum(text[i:].startswith('%s') for i in range(len(text)))
            values = [self.par1, self.par2, self.par3][:count]
            return self.logid.logtext.replace('%s', '{}').format(*values)
        else:
            return self.par1

    class Meta:
        db_table = 'inducks_log'


class LogData(models.Model):
    logid = models.CharField(max_length=4, primary_key=True)
    category = models.IntegerField(blank=True, null=True)
    logtext = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_logdata'
