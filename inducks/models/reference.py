from django.db import models

from inducks.models import helpers


class ReferenceReason(models.Model):
    referencereasonid = models.IntegerField(primary_key=True)
    referencereasontext = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_referencereason'


class ReferenceReasonName(models.Model):
    referencereason = helpers.InducksForeignKey('ReferenceReason', related_name='reason_names',
                                                isv_field='referencereasonid')
    language = helpers.InducksForeignKey('Language')
    referencereasontranslation = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_referencereasonname'
        unique_together = ['referencereason', 'language']


class StoryReference(models.Model):
    fromstory = helpers.InducksForeignKey('Story', related_name='references_from', db_column='fromstorycode')
    tostory = helpers.InducksForeignKey('Story', related_name='references_to', db_column='tostorycode')
    referencereason = helpers.InducksForeignKey('ReferenceReason', 'story_references', isv_field='referencereasonid')

    class Meta:
        db_table = 'inducks_storyreference'
        unique_together = ['fromstory', 'tostory']
