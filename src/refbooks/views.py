from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Element, Refbook, Version
from .serializers import (
    ElementSerializer,
    RefbookSerializer,
    VersionSerializer,
)


class RefbooksViewSet(ReadOnlyModelViewSet):
    queryset = Refbook.objects.all()
    serializer_class = RefbookSerializer

    def get_queryset(self):
        date_papam = self.request.query_params.get("date")
        if date_papam:
            return self.queryset.filter(versions__start_date__lte=date)
        return self.queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"refbooks": response.data})


class VersionsViewSet(ReadOnlyModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer


class ElementViewSet(ReadOnlyModelViewSet):
    serializer_class = ElementSerializer

    def get_version(self):
        refbook = get_object_or_404(Refbook, pk=self.kwargs.get("id"))
        version_param = self.request.query_params.get("version")
        if not version_param:
            return (
                refbook.versions.filter(start_date__lte=date.today())
                .order_by("-start_date")
                .first()
            )
        return refbook.versions.filter(version=version_param).first()

    def get_queryset(self):
        version = self.get_version()
        return version.elements
