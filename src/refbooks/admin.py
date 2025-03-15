from datetime import date

from django.contrib import admin

from .models import Element, Refbook, Version


class VersionInline(admin.TabularInline):
    model = Version
    extra = 0


class ElementInline(admin.TabularInline):
    model = Element
    extra = 0


class RefbookAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "code", "version", "start_date"]
    list_display_links = ("name",)
    search_fields = ("name", "code")
    inlines = [VersionInline]

    @admin.display(description="Версия")
    def version(self, obj):
        return (
            obj.versions.filter(start_date__lte=date.today())
            .order_by("-start_date")
            .first()
        )

    @admin.display(description="Дата начала действия")
    def start_date(self, obj):
        return self.version(obj).start_date


class VersionAdmin(admin.ModelAdmin):
    list_display = ["refbook__code", "refbook__name", "version", "start_date"]
    list_display_links = ("version", "refbook__name")
    search_fields = ("refbook", "version")
    inlines = [ElementInline]


admin.site.register(Refbook, RefbookAdmin)
admin.site.register(Version, VersionAdmin)
