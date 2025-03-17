from django.test import Client, TestCase

from refbooks.exceptions import (
    ElementDoesNotExist,
    RefbookDoesNotExist,
    VersionDoesNotExist,
)

from .test_data import (
    all_refbooks,
    current_version_elements,
    current_vertion_code,
    current_vertion_value,
    date_gte,
    date_lt_all,
    date_lt_one,
    existing_code,
    existing_refbook,
    existing_value,
    existing_version,
    existing_version_elements,
    not_existing_refbook,
    not_existing_value,
    not_existing_version,
)


class TestUrls(TestCase):
    fixtures = ["data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.client = Client()

    def test_refbooks_list(self):
        """Просмотр списка справочников без параметров (все справочники)."""
        response = self.client.get("/refbooks/")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data.get("refbooks"), list)
        assert len(resp_data.get("refbooks")) == all_refbooks

    def test_refbooks_date_today(self):
        """Просмотр списка справочников с параметром date => существующих."""
        response = self.client.get(f"/refbooks/?date={date_gte}")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data.get("refbooks"), list)
        assert len(resp_data.get("refbooks")) == all_refbooks

    def test_refbooks_date_yesterday(self):
        """Просмотр списка справочников с параметром date < одного из существующих."""
        response = self.client.get(f"/refbooks/?date={date_lt_one}")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data.get("refbooks"), list)
        assert len(resp_data.get("refbooks")) == all_refbooks - 1

    def test_refbooks_date_before(self):
        """Просмотр списка справочников с параметром date < всех существующих."""
        response = self.client.get(f"/refbooks/?date={date_lt_all}")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data.get("refbooks"), list)
        assert len(resp_data.get("refbooks")) == 0

    def test_refbooks_elements(self):
        """Просмотр списка элементов справочника без параметров (текущая версия)."""
        response = self.client.get(f"/refbooks/{existing_refbook}/elements/")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data.get("elements"), list)
        assert len(resp_data.get("elements")) == current_version_elements

    def test_not_existing_refbook(self):
        """Просмотр списка элементов несуществующего справочника."""
        response = self.client.get(f"/refbooks/{not_existing_refbook}/elements/")
        self.assertEqual(response.status_code, 404)
        resp_data = response.json()
        assert isinstance(resp_data, dict)
        assert len(resp_data) == 1
        assert resp_data.get("detail") == RefbookDoesNotExist().detail

    def test_refbooks_version_element(self):
        """Просмотр списка элементов справочника существующей версии."""
        response = self.client.get(
            f"/refbooks/{existing_refbook}/elements/?version={existing_version}"
        )
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data.get("elements"), list)
        assert len(resp_data.get("elements")) == existing_version_elements

    def test_refbooks_not_existing_version_element(self):
        """Просмотр списка элементов справочника несуществующей версии."""
        response = self.client.get(
            f"/refbooks/{existing_refbook}/elements/?version={not_existing_version}"
        )
        self.assertEqual(response.status_code, 404)
        resp_data = response.json()
        assert isinstance(resp_data, dict)
        assert len(resp_data) == 1
        assert resp_data.get("detail") == VersionDoesNotExist().detail

    def test_refbooks_check_element(self):
        """Валидация элемента справочника для существующего элемента
        (в текущей версии)."""
        response = self.client.get(
            f"/refbooks/{existing_refbook}/check_element/"
            f"?code={current_vertion_code}&value={current_vertion_value}"
        )
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data, dict)
        assert len(resp_data) == 2
        assert resp_data.get("code") == current_vertion_code
        assert resp_data.get("value") == current_vertion_value

    def test_refbooks_check_not_existing_element(self):
        """Валидация элемента справочника для несуществующего элемента
        (в текущей версии)."""
        response = self.client.get(
            f"/refbooks/{existing_refbook}/check_element/?"
            f"code={existing_code}&value={not_existing_value}"
        )
        self.assertEqual(response.status_code, 404)
        resp_data = response.json()
        assert isinstance(resp_data, dict)
        assert len(resp_data) == 1
        assert resp_data.get("detail") == ElementDoesNotExist().detail

    def test_refbooks_check_element_version_not_exist(self):
        """Валидация элемента справочника для несуществующей версии."""
        response = self.client.get(
            f"/refbooks/{existing_refbook}/check_element/"
            f"?code={existing_code}&value={existing_value}"
            f"&version={not_existing_version}"
        )
        self.assertEqual(response.status_code, 404)
        resp_data = response.json()
        assert isinstance(resp_data, dict)
        assert len(resp_data) == 1
        assert resp_data.get("detail") == VersionDoesNotExist().detail

    def test_refbooks_check_element_with_version(self):
        """Валидация элемента справочника для существующей версии."""
        response = self.client.get(
            f"/refbooks/{existing_refbook}/check_element/"
            f"?code={existing_code}&value={existing_value}&version={existing_version}"
        )
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        assert isinstance(resp_data, dict)
        assert len(resp_data) == 2
        assert resp_data.get("code") == existing_code
        assert resp_data.get("value") == existing_value
