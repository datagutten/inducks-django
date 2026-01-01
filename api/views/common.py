from rest_framework import viewsets

from inducks import utils


class InducksReadonlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    paginate_by = 10
    paginate_by_param = 'page_size'
    # set MAX results per page
    max_paginate_by = 100

    def get_queryset(self):
        model = self.serializer_class.Meta.model

        if self.lookup_field == 'pk' and 'pk' in self.kwargs:
            self.kwargs['pk'] = utils.replace_dash(self.kwargs['pk'])
            return self.queryset

        params = build_query(self.request.query_params)
        queryset = model.objects.all()
        filtered = queryset.filter(**params)
        return filtered


def build_query(params):
    args = {}
    for key, value in params.items():
        if key == 'page':
            continue
        args[key] = value
    return args
