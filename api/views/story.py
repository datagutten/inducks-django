from inducks import models
from api import serializers
from api.views.common import InducksReadonlyModelViewSet


class StoryViewSet(InducksReadonlyModelViewSet):
    queryset = models.Story.objects.all()
    serializer_class = serializers.story.StorySerializer


class StoryVersionViewSet(InducksReadonlyModelViewSet):
    queryset = models.StoryVersion.objects.prefetch_related('jobs').all()
    serializer_class = serializers.story.StoryVersionSerializer
