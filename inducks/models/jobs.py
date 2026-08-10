from django.db import models
from inducks.models import helpers
from django.utils.translation import gettext_lazy as _


class EntryJob(models.Model):
    entry = helpers.InducksForeignKey('Entry', related_name='jobs')
    person = helpers.InducksForeignKey('Person', related_name='entry_jobs')
    transletcol = models.CharField(max_length=1, blank=True, null=True)
    entryjobcomment = models.TextField(blank=True, null=True)
    doubt = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_entryjob'
        constraints = [
            models.UniqueConstraint(
                fields=['entry', 'person', 'transletcol'], name='EntryJob'
            )]

    def role_name(self):
        roles = {
            'l': _('letterer'),
            't': _('translator'),
            'c': _('colorist'),
        }
        if self.transletcol in roles:
            return roles[self.transletcol]
        else:
            return None


class StoryJob(models.Model):
    storyversion = helpers.InducksForeignKey('StoryVersion', related_name='jobs')
    person = helpers.InducksForeignKey('Person', related_name='story_jobs')
    plotwritartink = models.CharField(max_length=1, blank=True, null=True)
    storyjobcomment = models.TextField(blank=True, null=True)
    indirect = helpers.InducksBooleanField()
    doubt = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_storyjob'
        constraints = [
            models.UniqueConstraint(
                fields=['storyversion', 'person', 'plotwritartink'], name='StoryJob'
            )]

    def role_name(self):
        roles = {
            'p': _('plot'),
            'w': _('writer'),
            'a': _('artist'),
            'i': _('inker'),
            'r': _('reference'),
            'm': _('maintainer'),
        }
        if self.plotwritartink in roles:
            return roles[self.plotwritartink]
        else:
            return None


class MovieJob(models.Model):
    movie = helpers.InducksForeignKey('Movie', related_name='jobs')
    person = helpers.InducksForeignKey('Person', related_name='movie_jobs')
    role = models.CharField(max_length=15, blank=True, null=True)
    moviejobcomment = models.TextField(blank=True, null=True)
    indirect = models.CharField(max_length=1, blank=True, null=True)
    doubt = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_moviejob'
        constraints = [
            models.UniqueConstraint(
                fields=['movie', 'person', 'role'], name='MovieJob'
            )]


class PublishingJob(models.Model):
    publisher = helpers.InducksForeignKey('Publisher', related_name='jobs', db_column='publisher',
                                          isv_field='publisherid')
    issue = helpers.InducksForeignKey('Issue', related_name='publishingJobs')
    publishingjobcomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_publishingjob'
        constraints = [
            models.UniqueConstraint(
                fields=['publisher', 'issue'], name='PublishingJob'
            )]


class IssueJob(models.Model):
    issue = helpers.InducksForeignKey('Issue', related_name='jobs')
    person = helpers.InducksForeignKey('Person', related_name='issueJobs')
    inxtransletcol = models.CharField(max_length=1)
    issuejobcomment = models.TextField(blank=True, null=True)
    doubt = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_issuejob'
        constraints = [
            models.UniqueConstraint(
                fields=['issue', 'person', 'inxtransletcol'], name='IssueJob'
            )
        ]
