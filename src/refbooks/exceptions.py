from rest_framework.exceptions import NotFound


class RefbookDoesNotExist(NotFound):
    def __init__(self, detail="Справочник не найден"):
        super().__init__(detail)


class ElementDoesNotExist(NotFound):
    def __init__(self, detail="Элемент не найден"):
        super().__init__(detail)


class VersionDoesNotExist(NotFound):
    def __init__(self, detail="Версия не найдена"):
        super().__init__(detail)
