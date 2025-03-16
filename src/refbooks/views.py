from datetime import date

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ReadOnlyModelViewSet

from .decorators import response_format
from .descriptions import (
    check_element_description,
    elements_description,
    refbooks_description,
)
from .models import Refbook
from .openapi_settings import (
    code_param,
    date_param,
    elements_response,
    elements_serializer_response,
    refbooks_response,
    value_param,
    version_param,
)
from .serializers import (
    ElementSerializer,
    RefbookSerializer,
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description=refbooks_description,
        manual_parameters=[date_param],
        responses={200: refbooks_response},
    ),
)
@response_format
class RefbooksViewSet(ReadOnlyModelViewSet):
    queryset = Refbook.objects.all()
    serializer_class = RefbookSerializer

    def get_queryset(self):
        date_papam = self.request.query_params.get("date")
        if date_papam:
            return self.queryset.filter(versions__start_date__lte=date_papam)
        return self.queryset


class VersionsViewSet(ReadOnlyModelViewSet):
    def get_version(self):
        refbook = get_object_or_404(
            Refbook, pk=self.kwargs.get("id") or self.kwargs.get("pk")
        )
        version_param = self.request.query_params.get("version")
        if not version_param:
            return (
                refbook.versions.filter(start_date__lte=date.today())
                .order_by("-start_date")
                .first()
            )
        return refbook.versions.filter(version=version_param).first()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description=elements_description,
        manual_parameters=[version_param],
        responses={200: elements_response},
    ),
)
@response_format
class ElementViewSet(VersionsViewSet, ReadOnlyModelViewSet):
    serializer_class = ElementSerializer

    def get_queryset(self):
        version = self.get_version()
        return version.elements


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description=check_element_description,
        manual_parameters=[version_param, code_param, value_param],
        responses={200: elements_serializer_response},
    ),
)
class CheckElementViewSet(VersionsViewSet, ReadOnlyModelViewSet):
    serializer_class = ElementSerializer

    def get_queryset(self):
        version = self.get_version()
        code = self.request.query_params.get("code")
        value = self.request.query_params.get("value")
        return version.elements.filter(code=code, value=value)

    def get_object(self):
        return self.get_queryset().first()
