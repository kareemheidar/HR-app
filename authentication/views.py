from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import candAccount

# Create your views here.
def home(request):
    return render(request, 'Homepage.html')

def jobs(request):
    return render(request, 'jobs.html')

def application(request):
    return render(request, 'application.html')

def login(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        return render(request, 'jobs.html')
    return render(request, 'Login.html')

def logout(request):
    return render(request, 'Homepage.html')

def addCand(request):
    if(request.method == 'POST'):
        candID = request.POST['candID']
        username = request.POST['username']
        password = request.POST['password']
        candAcc = candAccount(candID = candID, username = username, password = password)
        candAcc.save()
        return render(request, 'Homepage.html')