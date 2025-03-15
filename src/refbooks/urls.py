from django.urls import include, path, register_converter
from rest_framework.routers import DefaultRouter

from src.converters import DateConverter

from .views import ElementViewSet, RefbooksViewSet

register_converter(DateConverter, "yyyy_mm_dd")


router = DefaultRouter()
router.register("refbooks", RefbooksViewSet, basename="refbooks")
router.register("refbooks?date=<yyyy_mm_dd:date>", RefbooksViewSet, basename="date")
router.register(r"refbooks/(?P<id>\d+)/elements", ElementViewSet, basename="elements")
router.register(
    r"refbooks/(?P<id>\d+)/elements?version=<version>",
    ElementViewSet,
    basename="version",
)
router.register(
    r"refbooks/(?P<id>\d+)/check_element?code=<code>&value=<value>",
    ElementViewSet,
    basename="check_element",
)
router.register(
    r"refbooks/(?P<id>\d+)/check_element?code=<code>&value=<value>&version=<version>",
    ElementViewSet,
    basename="check_element_version",
)

urlpatterns = [
    path("", include(router.urls)),
]
