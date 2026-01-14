from decimal import Decimal
from urllib.parse import urlparse
from requests.exceptions import HTTPError
import requests
import os

from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile

from places.models import Place, PlaceImage


def get_filename(url):
    path = urlparse(url).path
    return os.path.basename(path)


def replace_images(images_links, place):
    place.images.all().delete()
    for index, url in enumerate(images_links, start=1):
        image_response = requests.get(url)
        if image_response.status_code != 200:
            continue
        filename = get_filename(url)
        PlaceImage.objects.create(
            place=place,
            img=ContentFile(image_response.content, name=filename),
            order=index,
        )


class Command(BaseCommand):
    help = "Upload a new place to db by link"

    def add_arguments(self, parser):
        parser.add_argument("link", type=str)

    def handle(self, *args, **options):
        response = requests.get(options["link"])
        try:
            response.raise_for_status()
        except HTTPError:
            error_message = f"Ошибка {response.status_code} при подключении к {options["link"]}"
            raise CommandError(error_message)

        response_payload = response.json()

        lat = Decimal(response_payload["coordinates"]["lat"]).quantize(Decimal('0.000001'))
        lng = Decimal(response_payload["coordinates"]["lng"]).quantize(Decimal('0.000001'))

        place, created = Place.objects.update_or_create(
            title=response_payload["title"],
            lng=lng,
            lat=lat,
            defaults={
                "short_description": response_payload["description_short"],
                "long_description": response_payload["description_long"],
            }
        )

        replace_images(response_payload["imgs"], place)

        self.stdout.write(
            self.style.SUCCESS("Новая запись успешно добавлена в БД" if created
                               else "Запись успешно обновлена в БД")
        )
