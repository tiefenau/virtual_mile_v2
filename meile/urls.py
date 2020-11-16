from django.urls import path

from . import views

urlpatterns= [
    path('',views.index, name='index'),
    path('its_me/<slug:name>', views.its_me, name='its_me'),
    path('trinken', views.trinken, name='trinken'),
    path('pruegel/<slug:geschlagen>', views.pruegel, name='pruegel')
]