from django.db import models

# Create your models here.


class Place(models.Model):
    title = models.CharField("Название", max_length=80)
    description_short = models.CharField("Короткое описание", max_length=300)
    description_long = models.TextField("Описание")
    lng = models.DecimalField("Долгота", max_digits=18, decimal_places=14)
    lat = models.DecimalField("Широта", max_digits=18, decimal_places=14)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title