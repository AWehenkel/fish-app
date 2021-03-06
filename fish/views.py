import os
import pandas as pd
from django_pandas.io import read_frame
from mimetypes import MimeTypes
from django.http import Http404


from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import JsonResponse, HttpResponse
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper

from .models import Fish, Aquarium, FishDetection, NewFish, FishPosition
from .forms import FishForm, AquariumForm

from datetime import datetime

@login_required
def home_page(request):
    fishes = Fish.objects
    return render(request, 'fishapp/index.html', {'fishes': fishes})

@login_required
def data_monitor(request):
    anchor = ""
    if request.method == "POST":
        data = request.POST
        last_detections = FishDetection.objects.all()
        last_positions = FishPosition.objects.all()
        form_values = data
        if "aquarium_raw" in data.keys():
            last_detections = last_detections.filter(aquarium_id__in=data["aquarium_raw"])
        if "time_to_raw" in data.keys() and data["time_to_raw"]:
            last_detections = last_detections.filter(creation_date__lte=datetime.strptime(data["time_to_raw"], '%Y-%m-%d')).all()
        if "time_from_raw" in data.keys() and data["time_from_raw"]:
            last_detections = last_detections.filter(creation_date__gte=datetime.strptime(data["time_from_raw"], '%Y-%m-%d')).all()
        if "order_by_raw" in data.keys() and data["order_by_raw"]:
            anchor = "raw"
            last_detections = last_detections.order_by(data["order_by_raw"])
        if "nb_results_raw" in data.keys() and data["nb_results_raw"]:
            last_detections = last_detections[:int(data["nb_results_raw"])]
        if "aquarium_position" in data.keys():
            last_positions = last_positions.filter(fish__aquarium_id__in=data["aquarium_position"])
        if "time_to_position" in data.keys() and data["time_to_position"]:
            last_positions = last_positions.filter(end_date__lte=datetime.strptime(data["time_to_position"], '%Y-%m-%d')).all()
        if "time_from_position" in data.keys() and data["time_from_position"]:
            last_positions = last_positions.filter(end_date__gte=datetime.strptime(data["time_from_position"], '%Y-%m-%d')).all()
        if "order_by_position" in data.keys() and data["order_by_position"]:
            anchor="fish"
            last_positions = last_positions.order_by(data["order_by_position"])
        if "nb_results_position" in data.keys() and data["nb_results_position"]:
            last_positions = last_positions[:int(data["nb_results_position"])]
    else:
        form_values = {}
        last_detections = FishDetection.objects.order_by('-id', )[:5]
        last_positions = FishPosition.objects.order_by('-id', )[:5]

    aquariums = Aquarium.objects.all()
    read_frame(last_detections).to_csv("data_raw.csv")
    read_frame(last_positions).to_csv("data_fish.csv")
    return render(request, 'fishapp/data_monitor.html', {'last_detections': last_detections, 'aquariums': aquariums,
    'form_values': form_values, 'last_positions': last_positions, 'anchor': anchor})

@login_required
def add_fish(request):
    if request.method == "POST":
        form = FishForm(request.POST)
        if form.is_valid():
            form.instance.register()
            return redirect('home_page')
    form = FishForm()
    return render(request, 'fishapp/add_fish_aquarium.html', {'form': form, 'name': "Fish"})

@login_required
def delete_fish(request, pk):
    query = Fish.objects.filter(active=True).all().query
    query.order_by = ['aquarium_id']
    active_fishes = QuerySet(query=query, model=Fish)
    query = Fish.objects.filter(active=False).all().query
    query.order_by = ['aquarium_id']
    dead_fishes = QuerySet(query=query, model=Fish)
    problem = ""
    if pk is not None:
        fish = get_object_or_404(Fish, pk=pk)
        fish.active = not(fish.active)
        if not fish.active or not active_fishes.filter(rfid=fish.rfid, aquarium_id=fish.aquarium_id):
            fish.save()
        else:
            problem = "Fish already present in this aquarium with this rfid."
    return render(request, 'fishapp/delete_fish.html', {'active_fishes': active_fishes, 'dead_fishes': dead_fishes, 'problem': problem})

@login_required
def add_aquarium(request):
        if request.method == "POST":
            form = AquariumForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home_page')
        form = AquariumForm()
        return render(request, 'fishapp/add_fish_aquarium.html', {'form': form, 'name': "Aquarium"})

@login_required
def delete_aquarium(request, pk):
    query = Aquarium.objects.filter(active=True).all().query
    query.order_by = ['name']
    aquarium_on = QuerySet(query=query, model=Aquarium)
    query = Aquarium.objects.filter(active=False).all().query
    query.order_by = ['name']
    aquarium_off = QuerySet(query=query, model=Aquarium)
    if pk is not None:
        aquarium = get_object_or_404(Aquarium, pk=pk)
        aquarium.active = not(aquarium.active)
        aquarium.save()
    return render(request, 'fishapp/delete_aquarium.html', {'aquarium_on': aquarium_on, 'aquarium_off': aquarium_off})

@login_required
def update_last_fish(request):
    rfid = NewFish.objects.order_by('-id', )[:1]
    data = {
        'rfid': rfid[0].rfid
    }
    return JsonResponse(data)

@login_required
def check_aquarium_fish(request):
    aquarium_id = request.GET.get('aquarium_id', None)
    fish_id = request.GET.get('fish_id', None)
    data = {
        'aquarium_ok': not Fish.objects.filter(active=True, aquarium_id=aquarium_id, rfid=fish_id).exists()
    }
    return JsonResponse(data)

@login_required
def download_data(request, file_type):
    path = "data_%s.csv" % file_type
    wrapper = FileWrapper(open(path, "r"))
    mime = MimeTypes()
    content_type = mime.guess_type(path)[0]
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize( path ) # not FileField instance
    response['Content-Disposition'] = 'attachment; filename=%s/' % \
                                       smart_str( os.path.basename( path ) ) # same here
    return response
