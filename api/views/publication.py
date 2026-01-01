from api import serializers
from api.views.common import InducksReadonlyModelViewSet
from inducks import models


class PublicationViewSet(InducksReadonlyModelViewSet):
    queryset = models.publication.Publication.objects.all()
    serializer_class = serializers.publication.PublicationSerializer
