from django.core.management.base import BaseCommand

from inducks.importer.isv_import import IsvImport


class Command(BaseCommand, IsvImport):
    bulk = False

    def add_arguments(self, parser):
        parser.add_argument('--table', nargs='?', type=str)
        parser.add_argument('--force', nargs='?', type=bool, default=False)
        parser.add_argument('--dependencies', nargs='?', type=str, default=True)

    def handle(self, *args, **options):
        force = options['force'] is not False
        dependencies = options['dependencies'] != 'false'
        self.deptools.build_dependency_tree()

        if options['table']:
            if dependencies:
                self.import_with_dependencies(options['table'], force)
            else:
                self.import_table(options['table'], force)
        else:
            self.import_all(force)
