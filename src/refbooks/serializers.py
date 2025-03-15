from rest_framework import serializers

from .models import Element, Refbook, Version


class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        exclude = ["description"]


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ("code", "value")


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"
