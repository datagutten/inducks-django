import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, DatabaseError
from django.db.models import QuerySet

from inducks.models import jobs
from inducks.models import helpers

issuerangecode_cache = {}


class Issue(models.Model):
    issuecode = models.CharField(max_length=20, primary_key=True)
    issuerange = helpers.InducksForeignKey('IssueRange', related_name='issues', blank=True, null=True)
    publication = helpers.InducksForeignKey('Publication', related_name='issues')
    issuenumber = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=158, blank=True, null=True)
    size = models.CharField(max_length=82, blank=True, null=True)
    pages = models.CharField(max_length=93, blank=True, null=True)
    price = models.CharField(max_length=160, blank=True, null=True)
    printrun = models.CharField(max_length=142, blank=True, null=True)
    attached = models.CharField(max_length=288, blank=True, null=True)
    oldestdate = models.CharField(max_length=10, blank=True, null=True)
    fullyindexed = helpers.InducksBooleanField()
    issuecomment = models.CharField(max_length=1516, blank=True, null=True)
    error = helpers.InducksBooleanField()
    filledoldestdate = models.CharField(max_length=10, blank=True, null=True)
    locked = helpers.InducksBooleanField()
    inxforbidden = helpers.InducksBooleanField()
    inputfilecode = models.IntegerField(blank=True, null=True)
    maintenanceteamcode = models.CharField(max_length=8, blank=True, null=True)

    # maintenanceteam = helpers.InducksForeignKey('Team', related_name='issues', blank=True, null=True)

    class Meta:
        db_table = 'inducks_issue'

    def issuerangecode_helper(self, value):
        if value in issuerangecode_cache:
            self.issuerange = issuerangecode_cache[value]
            return

        try:
            self.issuerange = IssueRange.objects.get(issuerangecode=value)
            issuerangecode_cache[value] = self.issuerange
        except IssueRange.DoesNotExist:
            if not value:
                return
            # Try to create IssueRange if it does not exist
            obj = IssueRange(issuerangecode=value)
            publicationcode = re.sub(r'(.+)\s.+', r'\1', value)
            obj.publication_id = publicationcode
            try:
                obj.save()
                print('Created missing issuerangecode %s' % value)
            except DatabaseError:
                return
            self.issuerange = obj
            issuerangecode_cache[value] = obj

    def get_jobs(self, job_type):
        return jobs.IssueJob.objects.filter(issue_id=self.issuecode, inxtransletcol=job_type)

    def indexers(self):
        return self.get_jobs('i')

    def translators(self):
        return self.get_jobs('t')

    @property
    def year(self):
        date = self.dates.first()
        if date:
            return date.year()
        else:
            return None

    @property
    def full_title(self):
        if not self.title:
            return ' '.join([self.publication.title, self.issuenumber])
        else:
            return '%s %s - %s' % (self.publication.title, self.issuenumber, self.title)

    def cover(self):
        try:
            return self.entries.get(position='a')
        except ObjectDoesNotExist:
            return None


class IssueCollecting(models.Model):
    collectingissue = helpers.InducksForeignKey('Issue', 'collected', db_column='collectingissuecode',
                                                isv_field='collectingissuecode')
    collectedissue = helpers.InducksForeignKey('Issue', 'collecting', db_column='collectedissuecode',
                                               isv_field='collectedissuecode')

    class Meta:
        db_table = 'inducks_issuecollecting'
        unique_together = ['collectingissue', 'collectedissue']


class IssueDate(models.Model):
    issue = helpers.InducksForeignKey('Issue', related_name='dates')
    date = models.CharField(max_length=10)
    kindofdate = models.CharField(max_length=76, blank=True, null=True)
    doubt = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_issuedate'
        unique_together = ['issue', 'date']

    def year(self):
        return self.date[0:4]

    def __str__(self):
        return self.date


class IssuePrice(models.Model):
    issue = helpers.InducksForeignKey('Issue', related_name='prices')
    amount = models.CharField(max_length=86, blank=True, null=True)
    currency = models.CharField(max_length=14, blank=True, null=True)
    comment = models.CharField(max_length=75, blank=True, null=True)
    sequencenumber = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_issueprice'
        unique_together = ['issue', 'amount']


class IssueRange(models.Model):
    issuerangecode = models.CharField(max_length=15, primary_key=True)
    publication = helpers.InducksForeignKey('Publication', related_name='issueranges')
    title = models.CharField(max_length=228, blank=True, null=True)
    circulation = models.CharField(max_length=6, blank=True, null=True)
    issuerangecomment = models.CharField(max_length=468, blank=True, null=True)
    numbersarefake = helpers.InducksBooleanField(default=False)
    error = helpers.InducksBooleanField(default=False)

    class Meta:
        db_table = 'inducks_issuerange'


class Entry(models.Model):
    entrycode = models.CharField(max_length=22, primary_key=True)
    issue = helpers.InducksForeignKey('Issue', related_name='entries', blank=True, null=True)
    storyversion = helpers.InducksForeignKey('StoryVersion', related_name='entries', blank=True, null=True)
    language = helpers.InducksForeignKey('Language', null=True, blank=True)
    includedinentrycode = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=15, blank=True, null=True)
    printedcode = models.CharField(max_length=88, blank=True, null=True)
    guessedcode = models.CharField(max_length=39, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    reallytitle = helpers.InducksBooleanField()
    printedhero = models.CharField(max_length=96, blank=True, null=True)
    changes = models.TextField(blank=True, null=True)
    cut = models.TextField(blank=True, null=True)
    minorchanges = models.TextField(blank=True, null=True)
    missingpanels = models.CharField(max_length=21, blank=True, null=True)
    mirrored = helpers.InducksBooleanField()
    sideways = helpers.InducksBooleanField()
    startdate = models.CharField(max_length=10, blank=True, null=True)
    enddate = models.CharField(max_length=10, blank=True, null=True)
    identificationuncertain = helpers.InducksBooleanField()
    alsoreprint = models.CharField(max_length=336, blank=True, null=True)
    part = models.CharField(max_length=5, blank=True, null=True)
    entrycomment = models.TextField(blank=True, null=True)
    error = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_entry'

    def image(self) -> 'EntryURL':
        urls: QuerySet = self.urls.filter(site_id='webusers')
        if urls:
            return urls.first()
        else:
            return None

    def storycode(self):
        return self.storyversion.storycode


class EntryCharacterName(models.Model):
    entry = helpers.InducksForeignKey('Entry', 'character_names')
    character = helpers.InducksForeignKey('Character', 'entry_names')
    charactername = models.CharField(max_length=131, blank=True, null=True)

    class Meta:
        db_table = 'inducks_entrycharactername'
        unique_together = ['entry', 'character']


class Equiv(models.Model):
    issue = helpers.InducksForeignKey('Issue', related_name='equiv')
    equivid = models.IntegerField(blank=True, null=True)
    equivcomment = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        db_table = 'inducks_equiv'
        unique_together = ['issue', 'equivid']
