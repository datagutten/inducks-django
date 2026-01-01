from rest_framework import serializers

from inducks import models


class CharacterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.localization.CharacterName
        exclude = []


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        exclude = []

    names = CharacterNameSerializer(many=True, read_only=True)
