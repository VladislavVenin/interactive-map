from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from .models import Place


def show_index(request):
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for place in Place.objects.all():
        place_data = {
            "type": "Feature",
            "geometry": {
                    "type": "Point",
                    "coordinates": [place.lng, place.lat]
                },

            "properties": {
                    "title": place.title,
                    "placeId": place.id,
                    "detailsUrl": reverse('place_data', args=[place.id])
                }
        }
        geojson_data["features"].append(place_data)
    context = {
        'geojson_data': geojson_data
    }

    return render(request, 'index.html', context)


def show_place_data(request, post_id):
    place = get_object_or_404(Place, id=post_id)
    imgs = []
    for img in place.images.all():
        imgs.append(img.img.url)
    place_data = {
        "title": place.title,
        "imgs": imgs,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lat": place.lat,
            "lng": place.lng,
        }
    }
    return JsonResponse(place_data)
