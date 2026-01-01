from api import serializers
from api.views.common import InducksReadonlyModelViewSet
from inducks import models


class IssueViewSet(InducksReadonlyModelViewSet):
    queryset = models.issue.Issue.objects.all()
    serializer_class = serializers.issue.IssueSerializer


class EntryViewSet(InducksReadonlyModelViewSet):
    queryset = models.issue.Entry.objects.all()
    serializer_class = serializers.issue.EntrySerializer
