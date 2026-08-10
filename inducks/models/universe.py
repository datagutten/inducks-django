from django.db import models

from inducks.models import helpers


class UniverseCharacterRelation(models.Model):
    universe = helpers.InducksForeignKey('Universe', related_name='characters')
    character = helpers.InducksForeignKey('Character', related_name='universes')

    class Meta:
        db_table = 'inducks_ucrelation'
        unique_together = ['universe', 'character']


class Universe(models.Model):
    universecode = models.CharField(max_length=50, primary_key=True)
    universecomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_universe'

    def __str__(self):
        return self.universecode


class UniverseName(models.Model):
    universe = helpers.InducksForeignKey('Universe', related_name='names')
    language = helpers.InducksForeignKey('Language')
    universename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'inducks_universename'
        unique_together = ['universe', 'language']
