from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import candAccount, cands
from .forms import candAccount,candidate
from django.contrib import messages
from django.db.models import QuerySet

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
    

def signup(request):
    
    if request.method == "POST":
        form = candAccount(request.POST)
        if form.is_valid():
            form.save()
            messages
    else:
        form = candAccount()

    return render(request, 'Admin.html', {'form': form})
 

def apply(request):
    if request.method == "POST":
        vfname = request.POST['fname']
        vaddress = request.POST['address']
        vmilitary_status = request.POST['military_status']
        vphone = request.POST['phone']
        vdob = request.POST['dob']
        vcv = request.FILES.get('cv')
        cands.objects.create(cv=vcv, fname=vfname, phone=vphone, address=vaddress, dob=vdob, military_status=vmilitary_status)
        return render(request, 'Homepage.html')


# def apply(request):
#     if request.method == "POST":
#         print('first if')
#         form = candidate(request.POST)
#         print(form)
#         if form.is_valid():
#             print('second if')
#             form.save()
#             print('saved')
#             messages
#     else:
#         print('else')
#         form = candidate()
#     print('only returns')
#     return render(request, 'Homepage.html', {'form': form})