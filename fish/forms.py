from django import forms

from .models import Fish, Aquarium

class FishForm(forms.ModelForm):
    class Meta:
        model = Fish
        fields = "__all__"

class AquariumForm(forms.ModelForm):
    class Meta:
        model = Aquarium
        fields = "__all__"
