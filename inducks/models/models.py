from django.db import models

from inducks.models import helpers


class HeroCharacter(models.Model):
    story = helpers.InducksForeignKey('Story', related_name='heroes')
    character = helpers.InducksForeignKey('Character', related_name='heroes', blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    doubt = helpers.InducksBooleanField(default=False)

    class Meta:
        db_table = 'inducks_herocharacter'
        constraints = [
            models.UniqueConstraint(
                fields=['story', 'character'], name='herocharacter'
            )
        ]

    def charactercode_helper(self, value):
        if value in ['-', '?', '->']:
            return
        self.character_id = value
        pass


class LogoCharacter(models.Model):
    entry = helpers.InducksForeignKey('Entry', related_name='logoCharacters')
    character = helpers.InducksForeignKey('Character')
    reallyintitle = helpers.InducksBooleanField()
    number = models.IntegerField(blank=True, null=True)
    logocharactercomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_logocharacter'
        unique_together = ['entry', 'character']


class Studio(models.Model):
    studiocode = models.CharField(max_length=23, primary_key=True)
    country = helpers.InducksForeignKey('Country', 'studios', blank=True, null=True)
    studioname = models.CharField(max_length=24, blank=True, null=True)
    city = models.CharField(max_length=12, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    othertext = models.CharField(max_length=94, blank=True, null=True)
    photofilename = models.CharField(max_length=18, blank=True, null=True)
    photocomment = models.TextField(blank=True, null=True)
    photosource = models.CharField(max_length=42, blank=True, null=True)
    studiorefs = models.CharField(max_length=204, blank=True, null=True)

    class Meta:
        db_table = 'inducks_studio'


class StudioWork(models.Model):
    studio = helpers.InducksForeignKey('Studio')
    person = helpers.InducksForeignKey('Person')

    class Meta:
        db_table = 'inducks_studiowork'
        unique_together = ['studio', 'person']


class SubSeries(models.Model):
    subseriescode = models.CharField(max_length=60, primary_key=True)
    subseriesname = models.CharField(max_length=60, blank=True, null=True)
    official = helpers.InducksBooleanField()
    subseriescomment = models.TextField(blank=True, null=True)
    subseriescategory = models.CharField(max_length=46, blank=True, null=True)

    class Meta:
        db_table = 'inducks_subseries'


class SubSeriesName(models.Model):
    subseries = helpers.InducksForeignKey('SubSeries', related_name='names', isv_field='subseriescode')
    language = helpers.InducksForeignKey('Language')
    subseriesname = models.CharField(max_length=300, blank=True, null=True)
    preferred = helpers.InducksBooleanField()
    subseriesnamecomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_subseriesname'
        unique_together = ['subseries', 'language']


class Team(models.Model):
    teamcode = models.CharField(max_length=13, primary_key=True)
    teamdescriptionname = models.CharField(max_length=25, blank=True, null=True)
    teamshortname = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        db_table = 'inducks_team'


class TeamMember(models.Model):
    team = helpers.InducksForeignKey('Team', related_name='members')
    person = helpers.InducksForeignKey('Person', related_name='teams')

    class Meta:
        db_table = 'inducks_teammember'
        unique_together = ['team', 'person']


class InducksPrivEntry(models.Model):  # Not used
    entrycode = models.CharField(max_length=22, primary_key=True)
    entrycomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'induckspriv_entry'


class InducksPrivIssue(models.Model):  # Not used
    issuecode = models.CharField(max_length=16, primary_key=True)
    issuecomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'induckspriv_issue'


class InducksPrivStory(models.Model):  # Not used
    storycode = models.CharField(max_length=17, primary_key=True)
    storycomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'induckspriv_story'
