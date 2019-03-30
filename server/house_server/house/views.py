from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from house.models import RentHouse

def home(request):
    data = []
    for i in RentHouse.objects[:5]:
        data.append(i.price)
    return HttpResponse(data)
