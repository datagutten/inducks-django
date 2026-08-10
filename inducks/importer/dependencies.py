from typing import Type, Set, List, Iterable

import django.apps
from django.db.models import Model


class ModelDependencies:
    tiers: dict
    """
    Tiers with models
    """

    model_tiers: dict
    """
    Model tiers
    """

    @property
    def models(self):
        return django.apps.apps.get_models()

    @staticmethod
    def dependencies(model: Type[Model]):
        """
        Get model dependencies
        :param model:
        :return: List of table names
        """
        depends = []
        for field in model._meta.get_fields():
            if field.is_relation and (field.many_to_many or field.many_to_one):
                depends.append(field.related_model)

        return depends

    def dependencies_multi(self, model: Type[Model]) -> Set[Type[Model]]:
        dependencies = set()
        for dependency in self.dependencies(model):
            sub_dependencies = self.dependencies_multi(dependency)
            for sub_dependency in sub_dependencies:
                dependencies.add(sub_dependency)
            dependencies.add(dependency)
        return dependencies

    def sort_dependencies(self, dependencies: Iterable[Type[Model]]) -> list[Type[Model]]:
        """
        Sort dependencies by tier
        """
        tiers = {}
        dependencies_sorted = []
        for dependency in dependencies:
            tier = self.tier(dependency)
            if tier not in tiers:
                tiers[tier] = [dependency]
            else:
                tiers[tier].append(dependency)

        for tier in range(1, len(tiers) + 1):
            dependencies_sorted += tiers[tier]

        return dependencies_sorted

    def dependencies_sorted(self, model: Type[Model]) -> list[Type[Model]]:
        return self.sort_dependencies(self.dependencies_multi(model))

    @staticmethod
    def dependents(model: Type[Model]) -> Set[Type[Model]]:
        """
        Which models depends on the given model?
        """
        deps = set()
        for field in model._meta.get_fields():
            if field.is_relation and field.one_to_many:
                deps.add(field.related_model)
        return deps

    def has_dependencies(self, model: Type[Model]):
        deps = self.dependencies(model)
        return deps != []

    @property
    def base_models(self) -> List[Type[Model]]:
        """
        Tables with no dependencies
        """
        return [model for model in self.models if not self.has_dependencies(model)]

    def tier(self, model: Type[Model]):
        return self.model_tiers[model]

    def build_dependency_tree(self):
        tiers = {1: set(self.base_models)}
        table_tiers = dict(zip(tiers[1], [1] * len(tiers[1])))

        tier = 2
        while True:
            for table in tiers[tier - 1]:
                if tier not in tiers:
                    tiers[tier] = set()
                for dependent in self.dependents(table):
                    tiers[tier].add(dependent)

                    table_tiers[dependent] = tier
            if not tiers[tier]:
                break
            tier += 1
        tiers_final = {}

        for tier_iter in range(1, tier):
            tiers_final[tier_iter] = [table for table, tier2 in table_tiers.items() if tier2 == tier_iter]

        self.tiers = tiers_final
        self.model_tiers = table_tiers
        return tiers_final
