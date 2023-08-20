from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from .models import candidate_account, candidate, job, department
from django.contrib import messages
from django.db.models import QuerySet
import json


# Create your views here.
def home(request):
    return render(request, 'Homepage.html')

def jobs(request):
    jobs = job.objects.all()
    job_data = [
        {
            'id': job.jobID,
            'title': job.title,
            'description': job.description,
            'category': job.depID.depName
        }
        for job in jobs
    ]
    context = {
        'job_data_json': json.dumps(job_data)  # Convert job_data to JSON
    }
    return render(request, 'jobs.html', context)

def application(request):
    jobs = job.objects.all()
    job_data = [
        {
            'id': job.jobID,
            'title': job.title,
            'description': job.description,
            'category': job.depID.depName
        }
        for job in jobs
    ]
    context = {
        'all_jobs': json.dumps(job_data)
    }
    print("#################################################")
    print(context)
    return render(request, 'application.html')

def signin(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = candidate_account( username = username, password = password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'Homepage.html')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return render(request, 'jobs.html')
    return render(request, 'Login.html')


def logout(request):
    return render(request, 'Homepage.html')

def addCand(request):
    if(request.method == 'POST'):
        candID = request.POST['candID']
        username = request.POST['username']
        password = request.POST['password']
        candAcc = candidate_account(candID = candID, username = username, password = password)
        candAcc.save()
        return render(request, 'Homepage.html')
    


def apply(request):
    if request.method == "POST":
        vfname = request.POST['fname']
        vlname = request.POST['lname']
        vaddress = request.POST['address']
        vmilitary_status = request.POST['military_status']
        vphone = request.POST['phone']
        vdob = request.POST['dob']
        vcv = request.FILES.get('cv')
        vjobid = request.POST['jobID']
        vjob = job.objects.get( jobID = vjobid)
        print("EL JOB ID IS: ")
        print(vjobid)
        print("EL JOB ES: ")
        print(job)
        cand = candidate(cv=vcv, fname=vfname, lname=vlname, jobID=vjob, phone=vphone, address=vaddress, dob=vdob, military_status=vmilitary_status)
        cand.save()
        return render(request, 'Homepage.html')


def get_job_by_id(request, job_id):
    print('get_job_by_id')
    print("ENTERED GET JOB BY ID")
    jjob = job.objects.get(jobID=job_id)
    job_data = {
        'title': jjob.title,
        'description': jjob.description,
        'category': jjob.depID.depName,
    }
    return JsonResponse(job_data)

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