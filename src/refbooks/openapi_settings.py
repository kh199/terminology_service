from drf_yasg import openapi

from .descriptions import (
    date_param_description,
    elements_response_description,
    elements_serializer_description,
    refbooks_response_description,
    version_param_description,
)
from .serializers import (
    ElementSerializer,
    ElementsResponseSerializer,
    RefbooksResponseSerializer,
)

date_param = openapi.Parameter(
    "date",
    openapi.IN_QUERY,
    required=False,
    description=date_param_description,
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
    default="2020-01-01",
    pattern=r"\d{4}-\d{2}-\d{2}",
)
refbooks_response = openapi.Response(
    refbooks_response_description, RefbooksResponseSerializer
)
version_param = openapi.Parameter(
    "version",
    openapi.IN_QUERY,
    required=False,
    description=version_param_description,
    type=openapi.TYPE_STRING,
)
code_param = openapi.Parameter(
    "code",
    openapi.IN_QUERY,
    required=True,
    description="Код элемента",
    type=openapi.TYPE_STRING,
)
value_param = openapi.Parameter(
    "value",
    openapi.IN_QUERY,
    required=True,
    description="Значение элемента",
    type=openapi.TYPE_STRING,
)
elements_response = openapi.Response(
    elements_response_description, ElementsResponseSerializer
)
elements_serializer_response = openapi.Response(
    elements_serializer_description, ElementSerializer
)
