from api import serializers
from api.views.common import InducksReadonlyModelViewSet
from inducks import models


class LanguageViewSet(InducksReadonlyModelViewSet):
    queryset = models.localization.Language.objects.all()
    serializer_class = serializers.localization.LanguageSerializer
