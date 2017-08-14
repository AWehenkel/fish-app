from django import template
from django.contrib.auth.decorators import login_required
from ..models import Antenna

register = template.Library()

class ConnexionProblem:
    usb_problem = Antenna.objects.filter(usb_conection_check=False).all().filter(aquarium_id__active=True).all()
    antenna_problem = Antenna.objects.filter(usb_conection_check=True).all().filter(antenna_check=False).all().filter(aquarium_id__active=True).all()

    def nbProblem(self):
        return len(self.antenna_problem) + len(self.usb_problem)

    def update(self):
        self.usb_problem = Antenna.objects.all().filter(usb_conection_check=False).all().filter(aquarium_id__active=True)
        self.antenna_problem = Antenna.objects.filter(usb_conection_check=True).all().filter(antenna_check=False).all().filter(aquarium_id__active=True).all()
        return ""


@register.simple_tag
@login_required
def number_of_messages(request):
    return "coucou"

@register.assignment_tag(takes_context=True)
#@login_required
def usbProblem(context):
    return ConnexionProblem()
