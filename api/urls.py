import inspect
from typing import Type

from rest_framework import routers

from . import views
from .views.common import InducksReadonlyModelViewSet

app_name = 'inducks-api'

router = routers.DefaultRouter(trailing_slash=False, use_regex_path=False)

for mod_name, mod in inspect.getmembers(views):
    if not inspect.ismodule(mod):
        continue
    viewset: Type[InducksReadonlyModelViewSet]
    for viewset_name, viewset in inspect.getmembers(mod, inspect.isclass):
        if not issubclass(viewset, InducksReadonlyModelViewSet):
            continue
        if not hasattr(viewset, 'queryset') or not hasattr(viewset.queryset, 'model'):
            continue
        # noinspection PyProtectedMember
        basename = viewset.queryset.model._meta.db_table.replace('inducks_', '')
        router.register(basename, viewset, basename)
