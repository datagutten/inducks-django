import urllib.parse

from django.db import models

from inducks.models import helpers


class Site(models.Model):
    sitecode = models.CharField(max_length=16, primary_key=True)
    urlbase = models.CharField(max_length=51, blank=True, null=True)
    images = helpers.InducksBooleanField()
    sitename = models.CharField(max_length=85, blank=True, null=True)
    sitelogo = models.CharField(max_length=107, blank=True, null=True)
    properties = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'inducks_site'

    def __str__(self):
        return f'{self.sitename} ({self.sitecode})'

    def get_url_base(self):
        if self.urlbase.find('outducks') > -1:
            return 'https://inducks.org/hr.php?normalsize=1&image=%s' % (urllib.parse.quote(self.urlbase))
        else:
            return self.urlbase


class URLBase(models.Model):
    site = helpers.InducksForeignKey('Site')
    url = models.TextField(blank=True, null=True)

    def get_url(self):
        return self.site.get_url_base() + self.url

    def __str__(self):
        return self.get_url()

    class Meta:
        abstract = True


class CharacterURL(URLBase):
    character = helpers.InducksForeignKey('Character', related_name='urls')
    site = helpers.InducksForeignKey('Site', related_name='characters', blank=True, null=True)
    story = helpers.InducksForeignKey('Story', related_name='character_urls', blank=True, null=True)
    entry = helpers.InducksForeignKey('Entry', blank=True, null=True)

    class Meta:
        db_table = 'inducks_characterurl'
        unique_together = ['character', 'site']


class EntryURL(URLBase):
    entry = helpers.InducksForeignKey('Entry', related_name='urls')
    site = helpers.InducksForeignKey('Site', related_name='entries')
    pagenumber = models.IntegerField(blank=True, null=True)
    storycode = models.CharField(max_length=39, blank=True, null=True)
    public = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_entryurl'
        unique_together = ['entry', 'site', 'pagenumber']


class StoryURL(URLBase):
    story = helpers.InducksForeignKey('Story', related_name='urls')
    site = helpers.InducksForeignKey('Site', related_name='stories')

    class Meta:
        db_table = 'inducks_storyurl'
        unique_together = ['story', 'site']


class IssueURL(URLBase):
    issue = helpers.InducksForeignKey('Issue', related_name='urls')
    site = helpers.InducksForeignKey('Site', related_name='issues')

    class Meta:
        db_table = 'inducks_issueurl'
        unique_together = ['issue', 'site']


class PersonURL(URLBase):
    person = helpers.InducksForeignKey('Person', related_name='urls')
    site = helpers.InducksForeignKey('Site', related_name='persons')

    class Meta:
        db_table = 'inducks_personurl'
        unique_together = ['person', 'site']


class PublicationURL(URLBase):
    publication = helpers.InducksForeignKey('Publication', related_name='urls')
    site = helpers.InducksForeignKey('Site', related_name='publications')

    class Meta:
        db_table = 'inducks_publicationurl'
        unique_together = ['publication', 'site']
