from api import serializers
from api.views.common import InducksReadonlyModelViewSet
from inducks import models


class CharacterViewSet(InducksReadonlyModelViewSet):
    queryset = models.Character.objects.all()
    serializer_class = serializers.character.CharacterSerializer
