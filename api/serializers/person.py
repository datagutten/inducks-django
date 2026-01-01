from rest_framework import serializers

from inducks import models


class PersonAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.person.PersonAlias
        exclude = []


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.person.Person
        exclude = []

    aliases = PersonAliasSerializer(many=True, read_only=True)
