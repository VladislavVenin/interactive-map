from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField("Название", max_length=80)
    short_description = models.TextField("Короткое описание")
    long_description = HTMLField("Описание")
    lng = models.DecimalField("Долгота", max_digits=18, decimal_places=14)
    lat = models.DecimalField("Широта", max_digits=18, decimal_places=14)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        verbose_name="Место",
        related_name="images",
        on_delete=models.CASCADE
    )
    img = models.ImageField("Изображение")
    order = models.PositiveIntegerField(
        "Порядковый номер",
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        ordering = ('order',)
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f"{self.order} - {self.place.title}"
