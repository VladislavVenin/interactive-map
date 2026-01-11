# Сайт-афиша с интересными местами
Интерактивная карта с интересными местами рядом с вами
![browser_2026-01-12_07-38-25 (1)](https://github.com/user-attachments/assets/efabe614-c81f-42c5-b680-285b8bf6f416)

## Установка
Проект был собран на Python3

Установите зависимости
```
pip install -r requirements.txt
```
### Переменные окружения
Перед запуском веб-сервера требуется создать `.env` файл с следующими переменными окружения:
- [`SECRET_KEY`](https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-SECRET_KEY)
- `DEBUG` - True/False
- [`ALLOWED_HOSTS`](https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-ALLOWED_HOSTS)
- `DATABASE_FILEPATH` - Путь до вашей БД. По умолчаниею это `db.sqlite3` в корневом каталоге
## Запуск
Перед запуском используйте следующие команды:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
После этого вы можете запустить веб-сервер, он будет доступен по ссылке [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)
```
python manage.py runserver
```
### Добавление новых точек
Для добавления новых точек на карту воспользуйтесь командой `load_place`, она принимает на вход ссылку на `json файл` с данными о точке. Пример `json файла` можно посмотреть [здесь](https://github.com/VladislavVenin/interactive-map/blob/main/example.json).
```
python manage.py load_place https://github.com/VladislavVenin/interactive-map/blob/main/example.json
```
### Редактирование БД
Для редактирования базы данных требуется залогиниться в админку, для этого создайте пользователя с правами администратора:
```
python manage.py createsuperuser
```
Теперь перейдите по ссылке [`http://127.0.0.1:8000/admin`](http://127.0.0.1:8000/admin) и залогиньтесь.
![browser_2026-01-12_07-57-14](https://github.com/user-attachments/assets/211d1af1-05c7-4b2b-9d99-ebfa0e08ed73)

В админке вы можете свободно менять/создавать/удалять записи, добавлять/удалять новые картинки, менять их порядок, форматировать текст описания и т.д.
