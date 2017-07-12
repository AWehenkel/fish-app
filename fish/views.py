import os

from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet

from .models import Fish
from .forms import FishForm

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
    else:
        form = FishForm()
    form = FishForm()
    return render(request, 'fishapp/add_fish.html', {'form': form})

@login_required
def delete_fish(request, pk):
    query = Fish.objects.all().query
    query.group_by = ['aquarium']
    fishes = QuerySet(query=query, model=Fish)
    print(fishes)
    if pk is not None:
        fish = get_object_or_404(Fish, pk=pk)
        print(fish)
    return render(request, 'fishapp/delete_fish.html', {'fishes': fishes})

@login_required
def add_aquarium(request):
    return render(request, 'fishapp/add_aquarium.html')

@login_required
def delete_aquarium(request, pk):
    if pk is not None:
        aquarium = get_object_or_404(Aquarium, pk=pk)
        print(aquarium)
    return render(request, 'fishapp/delete_aquarium.html')
