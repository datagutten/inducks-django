import datetime
import re

from django.core import exceptions
from django.db import models


class InducksForeignKey(models.ForeignKey):
    isv_field: str = None

    def __init__(self, to: str, related_name=None, on_delete=models.PROTECT, **kwargs):
        if type(to) is not str:
            raise ValueError('Referenced model must be str')

        if 'isv_field' in kwargs:
            self.isv_field = kwargs['isv_field']
            del kwargs['isv_field']

        if 'db_column' not in kwargs:
            kwargs['db_column'] = to.lower() + 'code'

        super().__init__(to, on_delete, related_name=related_name, **kwargs)


class InducksBooleanField(models.BooleanField):
    # def from_db_value(self, value, expression, connection):
    #     return value == 'Y' or value == 1

    def to_python(self, value):
        try:
            return super().to_python(value)
        except exceptions.ValidationError as e:
            if value == 'Y':
                return True
            elif value == 'N':
                return False
            else:
                raise e


class InducksDateField(models.TextField):
    has_year = True
    has_month = False
    has_day = False

    def __init__(self, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 10
        super().__init__(**kwargs)

    def from_db_value(self, value, expression, connection):
        if not value:
            return

        matches = re.match(r'(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?', value)
        if not matches:
            print('Unable to parse date: %s' % value)
            return value
        year, month, day = matches.groups()
        if month:
            self.has_month = True
            month = int(month)
        else:
            month = 1

        if day:
            self.has_day = True
            day = int(day)
        else:
            day = 1

        try:
            return datetime.date(year=int(matches.group(1)), month=month, day=day)
        except TypeError:
            pass

    def to_python(self, value):
        try:
            return super().to_python(value)
        except exceptions.ValidationError as e:
            if value == '?':
                return None
            else:
                raise e
