from django.db import models
from django.db.models import QuerySet

import inducks.models as inducks_models
from . import helpers


class Character(models.Model):
    charactercode = models.CharField(max_length=120, primary_key=True)
    charactername = models.TextField(blank=True, null=True)
    official = helpers.InducksBooleanField()
    onetime = helpers.InducksBooleanField()
    heroonly = helpers.InducksBooleanField()
    charactercomment = models.TextField(blank=True, null=True)

    # appearances = models.ManyToManyField('InducksStoryVersion', through='InducksAppearance', through_fields=['charactercode', 'charactercode'])

    class Meta:
        db_table = 'inducks_character'

    def __str__(self):
        return self.charactername

    def common_names(self):
        return self.names.select_related('language').filter(preferred=True)

    def uncommon_names(self):
        return self.names.select_related('language').filter(preferred=False)

    def appearances(self):
        return Appearance.objects.filter(charactercode=self.charactercode).values_list('storyversion')

    def image_urls(self) -> QuerySet['inducks_models.CharacterURL']:
        return self.urls.filter(site_id='webusers-char0')


class Appearance(models.Model):
    storyversion = helpers.InducksForeignKey('StoryVersion', related_name='appearances')
    charactercode = models.TextField(max_length=69)  # unknown king on page 22 just next to GO
    number = models.IntegerField(blank=True, null=True)
    appearancecomment = models.TextField(blank=True, null=True)
    doubt = helpers.InducksBooleanField()

    def is_unknown(self):
        return self.charactercode[0] == '?'

    @property
    def character(self):
        if not self.is_unknown():
            return Character.objects.get(charactercode=self.charactercode)
        else:
            return None

    class Meta:
        db_table = 'inducks_appearance'
        unique_together = ['storyversion', 'charactercode']


class CharacterAlias(models.Model):
    character = helpers.InducksForeignKey('Character', 'aliases')
    charactername = models.CharField(max_length=58, primary_key=True)

    class Meta:
        db_table = 'inducks_characteralias'


class CharacterDetail(models.Model):
    charactername = models.CharField(max_length=7, primary_key=True)
    character = helpers.InducksForeignKey('Character', 'details')
    number = models.IntegerField()

    class Meta:
        db_table = 'inducks_characterdetail'


class CharacterReference(models.Model):
    fromcharacter = helpers.InducksForeignKey('Character', related_name='references_from',
                                              db_column='fromcharactercode')
    tocharacter = helpers.InducksForeignKey('Character', related_name='references_to', db_column='tocharactercode')
    isgroupofcharacters = helpers.InducksBooleanField()

    class Meta:
        db_table = 'inducks_characterreference'
        unique_together = ['fromcharacter', 'tocharacter']
