from rest_framework import serializers

from inducks import models
from .jobs import StoryJobSerializer


class StoryVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.story.StoryVersion
        exclude = ['appsummary']

    storyversioncode = serializers.CharField(read_only=True)
    storycode = serializers.CharField(read_only=True, source='story_id')
    appearances = serializers.PrimaryKeyRelatedField(read_only=True, many=True, source='appearances_characters')
    jobs = StoryJobSerializer(read_only=True, many=True)
    entries = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    plot = StoryJobSerializer(read_only=True, many=True)
    writer = StoryJobSerializer(read_only=True, many=True)
    art = StoryJobSerializer(read_only=True, many=True)
    ink = StoryJobSerializer(read_only=True, many=True)
    is_cover = serializers.BooleanField(read_only=True)
    kind_name = serializers.CharField(read_only=True)


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.story.Story
        exclude = []

    heroes = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='hero_characters')
    versions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    original_version = serializers.PrimaryKeyRelatedField(read_only=True, source='originalstoryversion')
    entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    issues = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    issuecodes = serializers.StringRelatedField(many=True)
