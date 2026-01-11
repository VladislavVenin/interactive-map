from django.shortcuts import render
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
                    "detailsUrl": "/static/places/moscow_legends.json"
                }
        }
        geojson_data["features"].append(place_data)
    context = {
        'geojson_data': geojson_data
    }

    return render(request, 'index.html', context)
