from rest_framework import serializers

from inducks import models


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publication
        exclude = ['error', 'locked']

    publicationcode = serializers.CharField(read_only=True)
    issues = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
