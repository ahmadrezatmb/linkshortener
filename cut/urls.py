from django.urls import path
from .views import beforcut,aftercut,  rd, all


urlpatterns = [
    path('' , beforcut , name='home'),
    path('aftercut' , aftercut , name='aftercut'),
    path('urls' , all),
    path('<str:number>' , rd),
]
