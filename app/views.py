from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
import csv
import urllib.parse


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    all_stations = []
    with open(settings.BUS_STATION_CSV, newline='', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_stations.append(row)

    paginator = Paginator(all_stations, 10)
    current_page = request.GET.get('page', 1)
    stations = paginator.get_page(current_page)

    prev_page, next_page = None, None
    prev_page_url, next_page_url = None, None

    if stations.has_previous():
        prev_page = stations.previous_page_number()
        pp = {'page': prev_page}
        url_page = urllib.parse.urlencode(pp)
        prev_page_url = reverse('bus_stations') + '?' + url_page
    if stations.has_next():
        next_page = stations.next_page_number()
        np = {'page': next_page}
        url_page = urllib.parse.urlencode(np)
        next_page_url = reverse('bus_stations') + '?' + url_page

    return render_to_response('index.html', context={
        'bus_stations': stations,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
