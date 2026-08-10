from typing import Type

from django.db import models

from inducks.models import helpers
import langcodes


class Language(models.Model):
    languagecode = models.CharField(max_length=7, primary_key=True)
    defaultlanguagecode = models.CharField(max_length=5, blank=True, null=True)
    languagename = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'inducks_language'

    def __str__(self):
        return self.languagename


class LanguageName(models.Model):
    desclanguagecode = models.CharField(max_length=5)
    language = helpers.InducksForeignKey('Language', 'names', blank=True, null=True)
    languagename = models.CharField(max_length=57, blank=True, null=True)

    class Meta:
        db_table = 'inducks_languagename'
        unique_together = ['desclanguagecode', 'language']

    def __str__(self):
        return self.languagename


class Country(models.Model):
    countrycode = models.CharField(max_length=2, primary_key=True)
    countryname = models.CharField(max_length=20, blank=True, null=True)
    defaultlanguage = helpers.InducksForeignKey('Language', 'countries', db_column='defaultlanguage', blank=True,
                                                null=True)
    defaultmaintenanceteam = helpers.InducksForeignKey('Team', 'countries', db_column='defaultmaintenanceteam',
                                                       blank=True, null=True)

    class Meta:
        db_table = 'inducks_country'

    def __str__(self):
        return self.countryname or self.countrycode


class CountryName(models.Model):
    country = helpers.InducksForeignKey('Country', related_name='names', blank=True, null=True)
    language = helpers.InducksForeignKey('Language')
    countryname = models.CharField(max_length=56)

    class Meta:
        db_table = 'inducks_countryname'
        unique_together = ['country', 'language']

    def __str__(self):
        if self.countryname:
            return self.countryname
        else:
            return super().__str__()


class Currency(models.Model):
    currencycode = models.CharField(max_length=3, primary_key=True)
    currencyname = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        db_table = 'inducks_currency'


class CurrencyName(models.Model):
    currency = helpers.InducksForeignKey('Currency', 'names')
    language = helpers.InducksForeignKey('Language')
    shortcurrencyname = models.CharField(max_length=19, blank=True, null=True)
    longcurrencyname = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'inducks_currencyname'
        unique_together = ['currency', 'language']


class CharacterName(models.Model):
    character = helpers.InducksForeignKey('Character', 'names')
    language = helpers.InducksForeignKey('Language')
    charactername = models.CharField(max_length=100, blank=True, null=True)
    preferred = helpers.InducksBooleanField()
    characternamecomment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inducks_charactername'
        unique_together = ['character', 'language', 'charactername']


def find_inducks_language(language) -> Type[Language]:
    lowest_distance = 999
    lowest_lang = None
    for lang in Language.objects.all():
        if lang.languagecode == language:
            return lang
        else:
            distance = langcodes.tag_distance(language, lang.languagecode)
            if distance < lowest_distance:
                lowest_lang = lang
                lowest_distance = distance
    if lowest_lang:
        return lowest_lang
    else:
        raise RuntimeError('Unable to find inducks language for code "%s"' % language)
