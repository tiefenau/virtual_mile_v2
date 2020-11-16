from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Trinker, Bier, Pruegel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'meile/index.html',{ "trinker": Trinker.objects.all()})

def its_me(request,name):
    t = Trinker.objects.get(user=name)
    return t.user

def trinken(request):
    b= Bier.objects.create(trinker=request.user.trinker)
    b.save()
    return redirect('/')

def pruegel(request,geschlagen):
    hauer = request.user
    geschlagen = User.objects.get(username=geschlagen)
    Pruegel.objects.create(schlaeger=hauer.trinker, geschlagen=geschlagen.trinker)
    return redirect('/')