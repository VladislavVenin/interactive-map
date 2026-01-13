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


def add_image_to_db(content, filename, place, order, path):
    if os.path.exists(path):
        image = PlaceImage.objects.get(img=filename)
        image_order = image.order
        image.delete()

        PlaceImage.objects.create(
            place=place,
            img=ContentFile(content, name=filename),
            order=image_order,
        )
    else:
        PlaceImage.objects.create(
            place=place,
            img=ContentFile(content, name=filename),
            order=order,
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
            lng=lat,
            lat=lng,
            defaults={
                "short_description": response_payload["description_short"],
                "long_description": response_payload["description_long"],
            }
        )
        start_index = place.images.count() + 1
        for index, url in enumerate(response_payload["imgs"], start=start_index):
            image_response = requests.get(url)
            if image_response.status_code == 200:
                filename = get_filename(url)

                path = f"media/{filename}"

                add_image_to_db(
                    image_response.content,
                    filename,
                    place,
                    index,
                    path
                )

        self.stdout.write(
            self.style.SUCCESS("Новая запись успешно добавлена в БД" if created
                               else "Запись успешно обновлена в БД")
        )
