from django.db import models
from django.utils import timezone

class Aquarium(models.Model):
    name = models.CharField(max_length=200)
    tank_nbr = models.IntegerField()
    usbs = models.TextField()
    temperatures = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def register(self):
        self.save()

    def __str__(self):
        return self.name

class Fish(models.Model):
    rfid = models.CharField(max_length=10)
    aquarium = models.ForeignKey('fish.Aquarium', related_name='fishes')
    creation_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    infected = models.BooleanField(default=False)
    note = models.TextField(default="")

    def register(self):
        self.save()

    def __str__(self):
        return self.rfid

class FishDetection(models.Model):
    fish_id = models.ForeignKey('fish.Fish', related_name='detections')
    aquarium_id = models.ForeignKey('fish.Aquarium', related_name='detections')
    antenna_number = models.IntegerField()
    creation_date = models.DateTimeField(default=timezone.now)
    duration =  models.FloatField()
    nb_detection = models.IntegerField()

    def register(self):
        self.save()

    def __str__(self):
        return self.fish_id

class NewFish(models.Model):
    rfid = models.CharField(max_length=10)

    def register(self):
        self.save()

    def __str__(self):
        return self.rfid

class Antenna(models.Model):
    aquarium_id = models.ForeignKey('fish.Aquarium', related_name='antenna')
    position = models.IntegerField()
    usb_conection_check = models.BooleanField()
    antenna_check = models.BooleanField(default=True)

    def register(self):
        self.save()

    def __str__(self):
        return "antenna_%d" % self.id
