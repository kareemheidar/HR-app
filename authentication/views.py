from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import candidate_account, candidate, job, department, background_images
from .forms import candidate_account
from django.contrib import messages
from django.db.models import QuerySet
import json
from datetime import datetime



# Create your views here.
def home(request):
    background_image = background_images.objects.first().homepage
    context = {
        'background_image': background_image
    }
    return render(request, 'Homepage.html', context)

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
    background_image = background_images.objects.first().application
    context = {
        'job_data_json': json.dumps(job_data),
        'background_image': background_image
    }
    return render(request, 'application.html', context)

def signin(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = candidate( username = username, password = password)
        user = authenticate(request, username=username, password=password)
        background_image = background_images.objects.first().login

        if user is not None:
            login(request, user)
            fname = user.first_name
            context = {
                'background_image': background_image,
                'fname': fname
            }
            return render(request, 'Homepage.html', context)
        else:
            messages.error(request, 'Username or Password is incorrect')
            return render(request, 'jobs.html')
    return render(request, 'Login.html')

def signout(request):
    logout(request)
    background_image = background_images.objects.first().homepage
    context = {
        'background_image': background_image
    }
    return render(request, 'Homepage.html', context)

def addCand(request):
    if(request.method == 'POST'):
        candID = request.POST['candID']
        username = request.POST['username']
        password = request.POST['password']
        candAcc = candidate_account(candID = candID, username = username, password = password)
        candAcc.save()
        return render(request, 'Homepage.html')
    

def age_calculator(dob):
    today = datetime.today()
    dob = datetime.strptime(dob, '%Y-%m-%d')
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def apply(request):
    if request.method == "POST":
        vfname = request.POST['fname']
        vlname = request.POST['lname']
        vaddress = request.POST['address']
        vemail = request.POST['email']
        vmilitary_status = request.POST['military_status']
        vphone = request.POST['phone']
        vdob = request.POST['dob']
        vcv = request.FILES.get('cv')
        vjobid = request.POST['jobID']
        vjob = job.objects.get( jobID = vjobid)
        vage = age_calculator(vdob)
        vjob.applicants_count = vjob.applicants_count + 1
        vjob.save()
        cand = candidate(cv=vcv, fname=vfname, lname=vlname, jobID=vjob, phone=vphone, address=vaddress, dob=vdob, military_status=vmilitary_status, email=vemail, age=vage,)
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