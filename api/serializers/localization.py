from rest_framework import serializers

from inducks import models


# Language
# LanguageName
# Country
# CountryName
# Currency
# CurrencyName

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.localization.Language
        exclude = []

    names = serializers.StringRelatedField(many=True, read_only=True)
