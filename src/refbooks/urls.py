from django.urls import path

from .views import CheckElementViewSet, ElementViewSet, RefbooksViewSet

urlpatterns = [
    path("refbooks/", RefbooksViewSet.as_view({"get": "list"})),
    path("refbooks/<int:id>/elements/", ElementViewSet.as_view({"get": "list"})),
    path(
        "refbooks/<int:pk>/check_element/",
        CheckElementViewSet.as_view({"get": "retrieve"}),
    ),
]
