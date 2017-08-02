from django.db import models
from django.utils import timezone


class FishPost(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

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
    rfid = models.CharField(max_length=30)
    aquarium = models.ForeignKey('fish.Aquarium', related_name='fishes')
    creation_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

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
