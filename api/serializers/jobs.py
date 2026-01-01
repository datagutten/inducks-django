from rest_framework import serializers

from inducks import models


class EntryJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntryJob
        exclude = []


class StoryJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoryJob
        exclude = []


class MovieJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieJob
        exclude = []


class PublishingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PublishingJob
        exclude = []


class IssueJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IssueJob
        exclude = []
