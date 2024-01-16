from django.urls import path
from rango import views

#rango directory
app_name = 'rango'

urlpatterns = [
    path('', views.index, name="index"),
]