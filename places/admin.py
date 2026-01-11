from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage


def preview_image(obj):
    if obj.img:
        return format_html('<img src="{}" height="200" />', obj.img.url)
    return "Нет изображения"


class ImageInline(admin.TabularInline):
    model = PlaceImage
    fields = ('place', 'order', 'img', 'image_preview')
    readonly_fields = ('image_preview',)
    extra = 1

    def image_preview(self, obj):
        return preview_image(obj)
    image_preview.short_description = "Фото"

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_short', 'lng', 'lat')
    search_fields = ('title',)
    inlines = [
        ImageInline,
    ]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'image_preview', 'order')
    list_display_links = ('place', 'image_preview')
    search_fields = ('place',)

    def image_preview(self, obj):
        return preview_image(obj)
    image_preview.short_description = "Фото"
