from django.core.management.base import BaseCommand
from django.core.files import File
from places.models import Place, PlaceImage
from urllib.parse import urlparse
import requests
import os


def get_filename(url):
    path = urlparse(url).path
    return os.path.basename(path)


def create_file(file_path, content):
    with open(file_path, "wb") as file:
        file.write(content)


def add_image_to_db(file_path, filename, place, order):
    with open(file_path, 'rb') as file:
        PlaceImage.objects.create(
            place=place,
            img=File(file, name=filename),
            order=order
        )


class Command(BaseCommand):
    help = "Upload a new place to db by link"

    def add_arguments(self, parser):
        parser.add_argument("link", type=str)

    def handle(self, *args, **options):
        response = requests.get(options["link"])
        response.raise_for_status()
        response_payload = response.json()

        place = Place.objects.get_or_create(
            title=response_payload["title"],
            description_short=response_payload["description_short"],
            description_long=response_payload["description_long"],
            lng=response_payload["coordinates"]["lng"],
            lat=response_payload["coordinates"]["lat"],
        )
        for index, url in enumerate(response_payload["imgs"], start=1):
            image_response = requests.get(url)
            if image_response.status_code == 200:
                filename = get_filename(url)
                file_path = f'media/{filename}'
                if not os.path.exists(file_path):
                    create_file(file_path, image_response.content)
                    add_image_to_db(file_path, filename, place[0], index)
                else:
                    add_image_to_db(file_path, filename, place[0], index)
                os.remove(file_path)

        self.stdout.write(
            self.style.SUCCESS("Новая запись успешно добавлена в БД")
        )
