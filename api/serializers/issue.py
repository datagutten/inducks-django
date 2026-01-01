from rest_framework import serializers

from inducks import models
from .story import StoryVersionSerializer


# Issue
# IssueCollecting
# IssueDate
# IssuePrice
# IssueRange
# Entry
# EntryCharacterName
# Equiv


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.issue.Issue
        exclude = ['inxforbidden', 'locked', 'inputfilecode', 'issuerange']

    entries = serializers.SlugRelatedField(many=True, read_only=True, slug_field='entrycode')
    year = serializers.IntegerField(read_only=True)
    full_title = serializers.CharField()


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.issue.Entry
        exclude = []

    issue = serializers.PrimaryKeyRelatedField(read_only=True)
    storyversion = StoryVersionSerializer(read_only=True)
    storycode = serializers.CharField(read_only=True)
    language = serializers.StringRelatedField(read_only=True)
