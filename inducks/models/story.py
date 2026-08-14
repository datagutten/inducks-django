from functools import cache
from typing import List

from django.db import models
from django.db.models import QuerySet
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

import inducks.models as inducks_models
from inducks.models import helpers


class Story(models.Model):
    storycode = models.CharField(max_length=19, primary_key=True)
    originalstoryversioncode = models.CharField(max_length=20, blank=True, null=True)
    creationdate = models.CharField(max_length=11, blank=True, null=True)
    firstpublicationdate = models.CharField(max_length=10, blank=True, null=True)
    endpublicationdate = models.CharField(max_length=10, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    usedifferentcode = models.CharField(max_length=20, blank=True, null=True)
    storycomment = models.TextField(blank=True, null=True)
    error = helpers.InducksBooleanField()
    repcountrysummary = models.TextField(blank=True, null=True)
    storyparts = models.IntegerField(blank=True, null=True)
    locked = helpers.InducksBooleanField()
    inputfilecode = models.IntegerField(blank=True, null=True)
    issuecodeofstoryitem = models.CharField(max_length=14, blank=True, null=True)
    maintenanceteamcode = models.CharField(max_length=10, blank=True, null=True)
    storyheadercode = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        db_table = 'inducks_story'

    @property
    def originalstoryversion(self) -> 'StoryVersion':
        return self.versions.get(storyversioncode=self.originalstoryversioncode)

    @cached_property
    def descriptions(self):
        return self.originalstoryversion.descriptions.all()

    def entries(self) -> List['inducks_models.Entry']:
        entries = []
        for version in self.versions.all():
            for entry in version.entries.all():
                entries.append(entry)

        return entries

    def issues(self) -> List['inducks_models.issue.Issue']:
        entries = []
        for version in self.versions.all():
            for entry in version.entries.all():
                entries.append(entry.issue)

        return entries

    def issuecodes(self):
        return [issue.issuecode for issue in self.issues()]

    def header(self):
        try:
            return StoryHeader.objects.get(storyheadercode=self.storyheadercode, level=0)
        except StoryHeader.DoesNotExist:
            return None

    def hero_characters(self):
        return [hero.character for hero in self.heroes.all()]


class StoryCreationDate(models.Model):
    story = helpers.InducksForeignKey('Story', 'creation_date')
    creationdate = models.CharField(max_length=10, null=True, blank=True)
    creationcomment = models.CharField(max_length=26, null=True, blank=True)

    class Meta:
        db_table = 'inducks_storycreationdate'
        unique_together = ['story', 'creationdate']


class StoryCodes(models.Model):
    story = helpers.InducksForeignKey('Story', related_name='storycodes')
    alternativecode = models.CharField(max_length=72, blank=True, null=True)
    unpackedcode = models.CharField(max_length=82, blank=True, null=True)
    codecomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_storycodes'
        unique_together = ['story', 'alternativecode']


class StoryDescription(models.Model):
    storyversion = helpers.InducksForeignKey('StoryVersion', related_name='descriptions')
    language = helpers.InducksForeignKey('Language')
    desctext = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_storydescription'
        unique_together = ['storyversion', 'language']


class StoryHeader(models.Model):
    storyheadercode = models.CharField(max_length=12)
    level = models.CharField(max_length=1, blank=True, null=True)
    title = models.CharField(max_length=96, blank=True, null=True)
    storyheadercomment = models.TextField(blank=True, null=True)
    countrycode = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        db_table = 'inducks_storyheader'
        unique_together = ['storyheadercode', 'level']
        ordering = ['storyheadercode', 'level']

    @staticmethod
    def get_helper(storyheadercode):
        try:
            return StoryHeader.objects.get(storyheadercode=storyheadercode, level=0)
        except StoryHeader.DoesNotExist:
            return StoryHeader.objects.get(storyheadercode=storyheadercode)


class StorySubSeries(models.Model):
    story = helpers.InducksForeignKey('Story', related_name='subseries')
    subseriescode = models.CharField(max_length=144, blank=True, null=True)
    storysubseriescomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_storysubseries'
        constraints = [
            models.UniqueConstraint(
                fields=['story', 'subseriescode'], name='StorySubSeries'
            )]


class StoryVersion(models.Model):
    """
    https://inducks.org/bolderbast/cct_inducks_storyversion.html
    """
    storyversioncode = models.CharField(max_length=50, primary_key=True)
    story = helpers.InducksForeignKey('Story', related_name='versions', blank=True, null=True)
    entirepages = models.IntegerField(blank=True, null=True)
    brokenpagenumerator = models.IntegerField(blank=True, null=True)
    brokenpagedenominator = models.IntegerField(blank=True, null=True)
    brokenpageunspecified = models.CharField(max_length=1, blank=True, null=True)
    kind = models.CharField(max_length=1, blank=True, null=True)
    """n = normal, k = newspaper strip, c = cover, i = illustration, etc."""
    rowsperpage = models.IntegerField(blank=True, null=True)
    columnsperpage = models.IntegerField(blank=True, null=True)
    appisxapp = models.CharField(max_length=1, blank=True, null=True)
    what = models.CharField(max_length=1, blank=True, null=True)
    """
    s = original story, c = changed, u = unidentified
    """
    appsummary = models.TextField(blank=True, null=True)
    plotsummary = models.TextField(blank=True, null=True)
    writsummary = models.TextField(blank=True, null=True)
    artsummary = models.TextField(blank=True, null=True)
    inksummary = models.TextField(blank=True, null=True)
    creatorrefsummary = models.TextField(blank=True, null=True)
    keywordsummary = models.TextField(blank=True, null=True)
    estimatedpanels = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_storyversion'

    @property
    def storycode(self):
        return self.story_id

    def plot_writ_art_ink(self, role):
        # return self.jobs.filter(plotwritartink=role)
        # return jobs.InducksStoryJob.objects.filter(plotwritartink=role, storyversion_id=self).select_related('person')
        jobs = []
        for job in self.jobs.all():
            if job.plotwritartink == role:
                jobs.append(job)
        return jobs

    @property
    def plot(self):
        return self.plot_writ_art_ink('p')

    @property
    def art(self):
        return self.plot_writ_art_ink('a')

    @property
    def ink(self):
        return self.plot_writ_art_ink('i')

    @property
    def writer(self):
        return self.plot_writ_art_ink('w')

    @property
    def is_cover(self):
        return self.kind == 'c'

    @property
    def is_gag(self):
        return self.kind == 'n' and 1 >= self.entirepages > 0

    @property
    def is_article(self):
        return self.kind == 'a'

    @property
    def is_illustration(self):
        return self.kind in [
            'i',  # Illustration
            'P'  # painting
        ]

    @property
    def is_unknown(self):
        return self.kind in ['f', 'g', 't', 'L']

    def kind_name(self) -> str:
        if self.kind == 'n':
            return ngettext_lazy('%d rows per page', '%d row per page', self.rowsperpage) % self.rowsperpage
        kinds = {
            'n': _('Story'),
            'k': _('Newspaper strip'),
            'i': _('Illustration'),
            'c': _('Cover'),
            'f': _('Centerfold'),
            't': _('Text story'),
            'a': _('Article'),
            'g': _('Game or puzzle'),
            's': _('Strange layout'),
            'L': _('Painting (landscape)'),
            'P': _('Painting (portrait)'),
        }
        if self.kind in kinds:
            return kinds[self.kind]
        else:
            return ''

    def images(self) -> QuerySet[inducks_models.Entry]:
        return self.entries.exclude(urls=None).filter(urls__site='webusers')

    def image(self):
        entry = self.images().first()
        if not entry:
            pass
        else:
            return entry.image()

    def appearances_characters(self) -> List['inducks_models.Character']:
        return [appearance.character for appearance in self.appearances.all()]


class SubStory(models.Model):
    storycode = models.CharField(max_length=20, primary_key=True)
    originalstoryversion = helpers.InducksForeignKey('StoryVersion', blank=True, null=True,
                                                     db_column='originalstoryversioncode')
    superstory = helpers.InducksForeignKey('Story', blank=True, null=True, related_name='substories',
                                           db_column='superstorycode'
                                           )
    part = models.IntegerField(blank=True, null=True)
    firstpublicationdate = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=101, blank=True, null=True)
    substorycomment = models.TextField(blank=True, null=True)
    error = helpers.InducksBooleanField()
    locked = helpers.InducksBooleanField()
    inputfilecode = models.IntegerField(blank=True, null=True)
    maintenanceteamcode = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        db_table = 'inducks_substory'
