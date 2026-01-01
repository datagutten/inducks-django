from api import serializers
from api.views.common import InducksReadonlyModelViewSet
from inducks import models


class PersonViewSet(InducksReadonlyModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.person.PersonSerializer


class PersonAliasViewSet(InducksReadonlyModelViewSet):
    queryset = models.PersonAlias.objects.all()
    serializer_class = serializers.person.PersonAliasSerializer
