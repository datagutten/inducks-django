import csv
import datetime
import re
from pathlib import Path
from typing import Callable, Type, Set

import django.apps
import django.db.models
import django.db.utils
from django.conf import settings
from django.core import exceptions
from django.db import DatabaseError
from django.db.models import Model

from inducks import models
from inducks import utils
from .dependencies import ModelDependencies


# noinspection PyProtectedMember
class IsvImport:
    imported: list = []
    """Imported tables"""

    keys: set = []
    """Keys for existing rows"""

    key_field: str
    """Name of the primary key field for the current table"""

    deptools: ModelDependencies = ModelDependencies()
    isv_path = settings.ISV_PATH

    @property
    def models(self):
        return django.apps.apps.get_models()

    def find_model(self, table: str) -> Type[django.db.models.Model]:
        """
        Find model from table name
        """
        for model in self.models:
            if model._meta.db_table == table:
                return model
        raise ModuleNotFoundError(table)

    def table_file(self, table: str) -> Path:
        """
        Get isv file for a table
        """
        return self.isv_path.joinpath(table).with_suffix('.isv')

    def table_list(self) -> list[str]:
        """
        Parse createtables.sql for table names
        :return: List of table names
        """
        tables = self.isv_path.joinpath('createtables.sql').read_text()
        matches = re.findall(r'LOAD DATA LOCAL INFILE "\./isv/.+" INTO TABLE (\w+)_temp', tables)
        return matches

    @staticmethod
    def get_model_field(model: Type[Model], db_column: str) -> django.db.models.Field:
        """Get model field object from database column name"""
        for field in model._meta.get_fields():
            if type(field).__name__ == 'ManyToOneRel':
                continue

            if hasattr(field, 'db_column') and field.db_column and field.db_column == db_column:
                return field
            elif field.attname == db_column:
                return field
        raise AttributeError('Unable to find model field for database column %s' % db_column)

    @staticmethod
    def get_field(model, key) -> str:
        if hasattr(model, key + '_helper'):
            return key

        try:
            is_relation = model._meta.get_field(key).is_relation
        except exceptions.FieldDoesNotExist:
            is_relation = True

        if is_relation:
            if key[-4:] == 'code':
                return '%s_id' % key[:-4]
            else:
                key = '%s_id' % key
        if not hasattr(model, key):
            for field in model._meta.get_fields():
                if hasattr(field, 'isv_field') and field.isv_field:
                    return field.attname

            raise AttributeError('Field %s not in model %s' % (key, model))
        else:
            return key

    def set_value(self, model: django.db.models.Model, field: str, value):
        """
        Set a model field value
        :param model:
        :param field:
        :param value:
        :return:
        """
        field = self.get_field(model, field)

        if hasattr(model, field + '_helper'):  # Check if there is a helper method for the field
            helper = getattr(model, field + '_helper')
            setattr(model, field, helper(value))
        else:
            setattr(model, field, value or None)

    def get_keys_set(self, model_class: Type[django.db.models.Model]) -> Set[str]:
        """
        Get existing keys from database
        :param model_class:
        :return:
        """
        self.key_field = model_class._meta.pk.attname
        keys = set(model_class.objects.values_list('pk', flat=True))
        try:
            # [keys.add(utils.clean_chars(key)) for key in self.keys]
            for key in list(keys):
                keys.add(utils.clean_chars(key))
        except AttributeError:
            pass
        return keys

    # def exist_check(self):

    def import_table(self, table: str, force: bool = False, filter_callback: Callable = None,
                     skip_existing: bool = True):
        if table in self.imported and not force:
            print('%s is already imported' % table)
            return
        file = self.table_file(table)
        if not file.exists():
            print('Input file not found: %s' % file)
            return
        print('%s: Preparing to import %s' % (datetime.datetime.now().isoformat(), table))
        with open(file, encoding='utf8') as fp:
            reader = csv.DictReader(fp, delimiter='^')
            model_class = self.find_model(table)  # Get the model class for the table
            self.keys = self.get_keys_set(model_class)

            # key_field = model_class._meta.pk.attname

            if not model_class:
                return
            if not force:
                try:
                    obj = model_class.objects.first()
                    if obj:
                        print('%s is already imported' % table)
                        self.imported.append(table)
                        return
                except django.db.utils.OperationalError as e:
                    print(e)
                    return

            row: dict
            print('%s: Importing %s' % (datetime.datetime.now().isoformat(), table))
            for row in reader:
                if filter_callback and not filter_callback(row):
                    continue

                print(f'{reader.line_num}\r', end='')
                if self.key_field in row:  # Some tables do not have a unique id in the source data
                    if skip_existing and self.key_field in row and row[self.key_field] in self.keys:
                        continue
                    # if skip_existing and self.keys_lower != [] and row[self.key_field].lower() in self.keys_lower:
                    #     continue
                    # if skip_existing and row[self.key_field] in self.keys:
                    #     continue
                    if type(row[self.key_field]) is str and row[self.key_field].lower() in self.keys:
                        continue

                model = model_class()
                for field, value in row.items():
                    if not field:
                        continue

                    field = self.get_field(model, field)

                    try:
                        if hasattr(model, field + '_helper'):  # Check if there is a helper method for the field
                            helper = getattr(model, field + '_helper')
                            setattr(model, field, helper(value))
                        else:
                            setattr(model, field, value or None)
                    except ValueError as e:
                        print(e)
                        continue

                try:
                    model.save()
                except DatabaseError as e:
                    if e.args[0] == 1062 or str(e).find('duplicate key value violates unique') > -1:
                        continue  # Duplicate entry
                    if e.args[0] == 1054:  # Unknown column
                        pass
                    if str(e).find('value too long') > -1:
                        print(str(e))
                        continue
                    if e.args[0] == 1406:
                        db_col = re.sub(r".+for column '(\w+)'.+", r'\1', str(e))
                        field = self.get_model_field(model, db_col)
                        print('Field %s is too short, should be at least %d characters to fit "%s"' % (
                            field, len(getattr(model, field.attname)), getattr(model, field.attname)))
                        continue  # Data too long

                    if e.args[0] == 1452 or str(e).find('violates foreign key constraint'):
                        matches = re.search(r'FOREIGN KEY \(`(\w+)`\) REFERENCES `(\w+)`', str(e))
                        if matches:
                            col, referenced_table = matches.groups()
                            field = self.get_model_field(model, col)

                            print('%s "%s" is not found in table %s' % (col, row[col], referenced_table))
                            if field.null:
                                setattr(model, field.attname, None)
                                model.save()
                            else:
                                print('%s: Field %s is not nullable, skipping row' % (table, field.attname))
                        else:
                            print('%s: %s' % (table, e))
                    else:
                        print(model)
                        print(e)
                except Exception as e:
                    print(model)
                    print(e)
                pass
            self.imported.append(table)
            print('%s: Import of %s completed' % (datetime.datetime.now().isoformat(), table))

    def import_with_dependencies(self, table, force=False):
        model = self.find_model(table)
        deps = self.deptools.dependencies_sorted(model)
        deps.append(model)
        for model in deps:
            self.import_table(model._meta.db_table, force=force)

    def import_tables(self, tables, recursive=False, force=False):
        for table in tables:
            if recursive:
                self.import_with_dependencies(table, force)
            else:
                self.import_table(table, force)

    def import_all(self, force=False):
        for tier, tier_models in self.deptools.tiers.items():
            for model in tier_models:
                self.import_table(model._meta.db_table, force)
                if model._meta.db_table == 'inducks_country':
                    models.Country(countrycode='zz').save()
