from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import candidate_account, candidate, job, department, background_images
from .forms import candidate_account
from django.contrib import messages
from django.db.models import QuerySet
import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMessage
from django.conf import settings


# Create your views here.
def home(request):
    background_image = background_images.objects.first().homepage
    context = {
        'background_image': background_image
    }
    return render(request, 'Homepage.html', context)

def aboutus(request):
    return render(request, 'aboutus.html')

def forgetpassword(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        user = candidate.objects.get(email=email)
        password = user.password

        email = EmailMessage(
                'Welcome to Madkour Group',
                'Your password is: ' + password + '\n' + 'Please login using the following link http://127.0.0.1:8000/login.',
                settings.EMAIL_HOST_USER,
                [email],
        )
        email.fail_silently = False
        email.send()
        messages.success(request, 'Your password has been sent to your email')
        return render(request, 'Login.html')
    return render(request, 'forgetpass.html')

def jobs(request):
    # get all jobs that are active
    jobs = job.objects.filter(is_active=True)
    deps = department.objects.all()
    job_data = [
        {
            'id': job.jobID,
            'title': job.title,
            'description': job.description,
            'category': job.depID.depName,
            'applicants_count': job.applicants_count,
            'years_of_experience': job.years_of_experience,
            'work_arrangement': job.work_arrangement,
            'location': job.location,
            'salary': job.salary,
            'date_posted': job.date_posted.strftime('%Y-%m-%d'),
            'level': job.level,

        }
        for job in jobs
    ]
    # get all unique work arrangements
    work_arrangements = job.objects.values_list('work_arrangement', flat=True).distinct()
    locs = job.objects.values_list('location', flat=True).distinct()
    context = {
        'job_data_json': json.dumps(job_data, cls=DjangoJSONEncoder) ,
        'departments': deps,
        'arrangements': work_arrangements,
        'locations': locs
    }
    return render(request, 'jobs.html', context)




def application(request):
    # get all jobs that are active
    jobs = job.objects.filter(is_active=True)
    job_data = [
        {
            'id': job.jobID,
            'title': job.title,
            'description': job.description,
            'category': job.depID.depName,
            'applicants_count': job.applicants_count,
            'years_of_experience': job.years_of_experience,
            'work_arrangement': job.work_arrangement,
            'location': job.location,
            'salary': job.salary,
            'date_posted': job.date_posted.strftime('%Y-%m-%d'),
            'level': job.level,

        }
        for job in jobs
    ]
    background_image = background_images.objects.first().application
    context = {
        'job_data_json': json.dumps(job_data, cls=DjangoJSONEncoder),
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
            cand = candidate.objects.get(email= user.email)
            fname=cand.fname
            status = cand.cand_status
            message=cand.Note
            job_id = cand.jobID_id
            jobx = job.objects.get(jobID=job_id)
            job_title= jobx.title
            job_description=jobx.description
            
            
            context = {
                #'background_image': background_image,
                'status':status,
                'message':message,
                'job_description':job_description,
                'job_title' :job_title,
                'fname':fname
            }
            return render(request, 'status.html', context)
            
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


"""def my_view(request):
    """
    #This view renders an HTML page with a div element. The border color of the div element will be red if the user has not seen or read it.
"""

    div_id = "my-div"

    # Get the current user
    user = request.user

    # Check if the user has seen or read the div element
    has_seen_or_read_div = False

    # If the user has not seen or read the div element, set the border color to red
    if not has_seen_or_read_div:
        css_border_color = "red"
    else:
        pass

    # Render the HTML page
    return render(request, "status.html", {
        "div_id": div_id,
        "css_border_color": css_border_color
    })"""






























# def register_candidate(modeladmin, request,queryset):
#     for candidate in queryset:
#         if candidate.username is not None and candidate.password is not None:
#             username = candidate.username
#             password = candidate.password
#             email=candidate.email
#             newuser=User.objects.create_user(username,email,password)
#             newuser.first_name=candidate.fname
#             newuser.last_name = candidate.lname
#             newuser.save()


"""def get_status(request,username):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = candidate.objects.get(username=username)
        status = user.cand_status
        Message = user.Note
        jobDetail=job.objects.get(jobID=user.jobID)
        jobDescription=jobDetail.description
        jobTitle="jobDetail.title"
        context = {
            'job_Title': jobTitle ,
            'job_description' : jobDescription , 
            'status' : status ,
            'Message' : Message
        }
    return render(request,'status.html',context)"""
    
    



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