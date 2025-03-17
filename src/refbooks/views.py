from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ReadOnlyModelViewSet

from .decorators import response_format
from .descriptions import (
    check_element_description,
    elements_description,
    refbooks_description,
)
from .methods import ElementMethods, VersionMethods
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
            return self.queryset.filter(versions__start_date__lte=date_papam).distinct()
        return self.queryset


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description=elements_description,
        manual_parameters=[version_param],
        responses={200: elements_response},
    ),
)
@response_format
class ElementViewSet(ReadOnlyModelViewSet):
    serializer_class = ElementSerializer

    def get_queryset(self):
        version = VersionMethods(self.request, self.args, self.kwargs).get_version()
        return version.elements


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description=check_element_description,
        manual_parameters=[version_param, code_param, value_param],
        responses={200: elements_serializer_response},
    ),
)
class CheckElementViewSet(ReadOnlyModelViewSet):
    serializer_class = ElementSerializer

    def get_queryset(self):
        return ElementMethods(self.request, self.args, self.kwargs).get_element()

    def get_object(self):
        return self.get_queryset().first()
