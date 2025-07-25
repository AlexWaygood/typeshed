from _typeshed import Incomplete
from typing import Any
from typing_extensions import TypeAlias

from django.db.models import Model, QuerySet

from .fields import Field
from .resources import Resource

Dataset: TypeAlias = Incomplete  # tablib.Dataset

class BaseInstanceLoader:
    """
    Base abstract implementation of instance loader.
    """

    resource: Resource[Any]
    dataset: Dataset | None
    def __init__(self, resource: Resource[Any], dataset: Dataset | None = None) -> None: ...
    def get_instance(self, row: dict[str, Any]) -> Model | None: ...

class ModelInstanceLoader(BaseInstanceLoader):
    """
    Instance loader for Django model.

    Lookup for model instance by ``import_id_fields``.
    """

    def get_queryset(self) -> QuerySet[Any]: ...

class CachedInstanceLoader(ModelInstanceLoader):
    """
    Loads all possible model instances in dataset avoid hitting database for
    every ``get_instance`` call.

    This instance loader work only when there is one ``import_id_fields``
    field.
    """

    pk_field: Field
    all_instances: dict[Any, Model]
