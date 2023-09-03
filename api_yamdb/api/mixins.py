from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsAdminOrAnonymous


class LookUpSlugFieldMixin:
    """
    Добавляет поле 'lookup_field' со значением 'slug'
    для создания url-путей с использованием 'slug' вместо 'id'.
    """
    class Meta:
        abstract = True
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин для добавления возможности создания,
    получения списка и удаления объектов модели.
    """
    ...


class CreateListDestroySearchViewSet(CreateListDestroyViewSet):
    """Миксин для добавления возможности поиска по полю и пермишенов."""
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrAnonymous,
    )