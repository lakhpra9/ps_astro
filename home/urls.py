from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_astrology', views.get_astrology, name='get_astrology'),
]