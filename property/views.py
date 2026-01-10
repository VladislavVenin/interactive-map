from django.http import HttpResponse


def show_index(request):
    return HttpResponse("<h1>Main page</h1>")