from datetime import date

from .exceptions import ElementDoesNotExist, RefbookDoesNotExist, VersionDoesNotExist
from .models import Refbook


class BaseMethods:
    def __init__(self, request, args, kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs


class RefbookMethods(BaseMethods):
    def get_refbook_by_id(self):
        try:
            return Refbook.objects.get(
                pk=self.kwargs.get("id") or self.kwargs.get("pk")
            )
        except Exception:
            raise RefbookDoesNotExist


class VersionMethods(RefbookMethods):
    def get_version(self):
        refbook = self.get_refbook_by_id()
        version_param = self.request.query_params.get("version")
        if not version_param:
            return (
                refbook.versions.filter(start_date__lte=date.today())
                .order_by("-start_date")
                .first()
            )
        version = refbook.versions.filter(version=version_param).first()
        if not version:
            raise VersionDoesNotExist
        return version


class ElementMethods(VersionMethods):
    def get_element(self):
        version = self.get_version()
        query_params = self.request.query_params
        element = version.elements.filter(
            code=query_params.get("code"), value=query_params.get("value")
        )
        if element:
            return element
        raise ElementDoesNotExist
