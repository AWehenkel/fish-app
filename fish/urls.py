from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^data_monitor$', views.data_monitor, name='data_monitor'),
    url(r'^add_fish$', views.add_fish, name='add_fish'),
    url(r'^delete_fish/((?P<pk>\d+)/)?$$', views.delete_fish, name='delete_fish'),
    url(r'^add_aquarium$', views.add_aquarium, name='add_aquarium'),
    url(r'^delete_aquarium/((?P<pk>\d+)/)?$$', views.delete_aquarium, name='delete_aquarium'),
    url(r'^ajax/update_last_fish/$', views.update_last_fish, name='update_last_fish'),
    url(r'^ajax/check_aquarium_fish/$', views.check_aquarium_fish, name='check_aquarium_fish'),
]
