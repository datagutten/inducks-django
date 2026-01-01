from api import serializers
from api.views.common import InducksReadonlyModelViewSet
from inducks import models


class EntryJobViewSet(InducksReadonlyModelViewSet):
    queryset = models.EntryJob.objects.all()
    serializer_class = serializers.jobs.EntryJobSerializer


class StoryJobViewSet(InducksReadonlyModelViewSet):
    queryset = models.StoryJob.objects.all()
    serializer_class = serializers.jobs.StoryJobSerializer


class MovieJobViewSet(InducksReadonlyModelViewSet):
    queryset = models.MovieJob.objects.all()
    serializer_class = serializers.jobs.MovieJobSerializer


class PublishingJobViewSet(InducksReadonlyModelViewSet):
    queryset = models.PublishingJob.objects.all()
    serializer_class = serializers.jobs.PublishingJobSerializer


class IssueJobViewSet(InducksReadonlyModelViewSet):
    queryset = models.IssueJob.objects.all()
    serializer_class = serializers.jobs.IssueJobSerializer
