from django.db import models

from inducks.models import helpers


class StatCharacterCharacter(models.Model):
    character = helpers.InducksForeignKey('Character')
    cocharactercode = models.CharField(max_length=58, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    yearrange = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'inducks_statcharactercharacter'
        unique_together = ['character', 'total']


class StatCharacterCountry(models.Model):
    character = helpers.InducksForeignKey('Character', 'country_stat')
    country = helpers.InducksForeignKey('Country', 'character_stat')
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_statcharactercountry'
        unique_together = ['character', 'country']


class StatCharacterStory(models.Model):
    character = helpers.InducksForeignKey('Character', 'story_stat')
    storyheader = helpers.InducksForeignKey('StoryHeader', 'character_stat', null=True)
    total = models.IntegerField(blank=True, null=True)
    yearrange = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'inducks_statcharacterstory'
        unique_together = ['character', 'storyheader']

    def storyheadercode_helper(self, value):
        from inducks.models import StoryHeader
        try:
            self.storyheader = StoryHeader.get_helper(value)
        except StoryHeader.DoesNotExist:
            return


class StatPersonCharacter(models.Model):
    person = helpers.InducksForeignKey('Person', 'character_stat')
    character = helpers.InducksForeignKey('Character', 'person_stat')
    total = models.IntegerField(blank=True, null=True)
    yearrange = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'inducks_statpersoncharacter'
        unique_together = ['person', 'total']


class StatPersonCountry(models.Model):
    person = helpers.InducksForeignKey('Person', 'country_stat')
    country = helpers.InducksForeignKey('Country', 'person_stat')
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_statpersoncountry'
        unique_together = ['person', 'country']


class StatPersonPerson(models.Model):
    person = helpers.InducksForeignKey('Person', 'co_stats_from')
    coperson = helpers.InducksForeignKey('Person', 'co_stats', blank=True, null=True, isv_field='copersoncode',
                                         db_column='copersoncode')
    total = models.IntegerField(blank=True, null=True)
    yearrange = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'inducks_statpersonperson'
        unique_together = ['person', 'total']


class StatPersonStory(models.Model):
    person = helpers.InducksForeignKey('Person', 'story_stat')
    storyheader = helpers.InducksForeignKey('StoryHeader', 'person_stat', null=True)
    total = models.IntegerField(blank=True, null=True)
    yearrange = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'inducks_statpersonstory'
        unique_together = ['person', 'storyheader']

    def storyheadercode_helper(self, value):
        from inducks.models import StoryHeader
        try:
            self.storyheader = StoryHeader.get_helper(value)
        except StoryHeader.DoesNotExist:
            return
