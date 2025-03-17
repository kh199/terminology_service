# Сервис терминологии

Стек:

```Python```
```Django```
```Django REST framework```
```PostgreSQL```
```Nginx```
```Docker```

Независимый сервис терминологии, который хранит коды данных и их контекст. 
Реализованы 3 сущности: Справочник, Версия, Элемент.

## Пример кодируемых данных
Справочник: Специальности медицинских работников.
Код справочника: 1
Версия справочника: 1.0
Дата публикации: 01.01.2022.
Элементы справочника (код - значение):
1 - Врач-терапевт
2 - Травматолог-ортопед
3 - Хирург

## Установка

Клонировать репозиторий:
```
git clone https://github.com/kh199/terminology_service
```
Создать и заполнить файл .env на основе .env.template

Запустить docker-compose:
```
docker-compose up -d
```
Выполнить миграции:
```
docker-compose exec terminology_app python manage.py migrate
```
Заполнить базу готовыми данными (опционально):
```
docker-compose exec web python manage.py loaddata data.json
```
Создать суперпользователя:
```
docker-compose exec terminology_app python manage.py createsuperuser
```
Подгрузить статику:
```
docker-compose exec terminology_app python manage.py collectstatic --no-input 
```
Запустить тесты:
```
docker-compose exec terminology_app python manage.py test
```

Панель администратора доступна по адресу ```http://127.0.0.1:8000/admin```
Документация доступна по адресу ```http://127.0.0.1:8000/swagger```

## Методы API

+ **GET**   ```refbooks/[?date=<date>]``` получение списка справочников (+ актуальных на указанную дату)
+ **GET**   ```refbooks/<id>/elements[?version=<version>]``` получение элементов заданного справочника
+ **GET**   ```refbooks/<id>/check_element?code=<code>&value=<value>[&version=<version>]``` проверка на то, что элемент с данным кодом и значением присутствует в указанной версии справочника
