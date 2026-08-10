import django.apps


class InducksImport:
    models: list = []

    def __init__(self):
        self.get_models()

    def get_models(self):
        for model in django.apps.apps.get_models():
            if model.__name__.find('Inducks') == -1:
                continue
            self.models.append(model)

    def find_model(self, table: str):
        for model in self.models:
            if model._meta.db_table == table:
                return model
            # if name.lower() == model.__name__.lower():
            #     return model
        raise ModuleNotFoundError(table)

    pass
