from django.db import models


class Refbook(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return self.name


class Version(models.Model):
    refbook = models.ForeignKey(
        Refbook,
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name="Справочник",
    )
    version = models.CharField(max_length=50, verbose_name="Версия")
    start_date = models.DateField(verbose_name="Дата начала действия")

    class Meta:
        ordering = ["version"]
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"
        constraints = [
            models.UniqueConstraint(
                fields=["refbook", "version"],
                name="unique_refbook_version",
            ),
            models.UniqueConstraint(
                fields=["refbook", "start_date"],
                name="unique_refbook_start_date",
            ),
        ]

    def __str__(self):
        return self.version


class Element(models.Model):
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        verbose_name="Версия",
        related_name="elements",
    )
    code = models.CharField(max_length=100, verbose_name="Код элемента")
    value = models.CharField(max_length=300, verbose_name="Значение элемента")

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"
        constraints = [
            models.UniqueConstraint(
                fields=["version", "code"],
                name="unique_version_code",
            ),
        ]

    def __str__(self):
        return self.code
