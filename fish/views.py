import os

from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet

from .models import Fish, Aquarium
from .forms import FishForm, AquariumForm

@login_required
def home_page(request):
    fishes = Fish.objects
    return render(request, 'fishapp/index.html', {'fishes': fishes})

@login_required
def data_monitor(request):
    return render(request, 'fishapp/data_monitor.html')

@login_required
def add_fish(request):
    if request.method == "POST":
        form = FishForm(request.POST)
        if form.is_valid():
            form.save()
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
    if pk is not None:
        fish = get_object_or_404(Fish, pk=pk)
        fish.active = not(fish.active)
        fish.save()
    return render(request, 'fishapp/delete_fish.html', {'active_fishes': active_fishes, 'dead_fishes': dead_fishes})

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
