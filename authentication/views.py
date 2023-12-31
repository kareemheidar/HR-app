from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import candidate_account, candidate, job, department, background_images , resume
from .forms import candidate_account
from django.contrib import messages
from django.db.models import QuerySet
import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
import csv
from django.http import FileResponse
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    background_image = background_images.objects.first().homepage
    context = {
        'background_image': background_image
    }
    return render(request, 'Homepage.html', context)

def temp(request):
    # create dummy data for a candidate and his job application
    context = {
        'fname': 'Ahmed',
        'lname': 'Mohamed',
        'email': 'ahmedmohamed@gmail.com',
        'address': 'Cairo, Egypt',
        'military_status': 'Exempted',
        'status': 'on stack',
        'message': 'We are sorry to inform you that you have been put on stack. We will contact you if a suitable position is available.',
        'phone': '01234567890',
        'dob': '1998-01-01',
        'age': 25,
        'cv': 'cv.pdf',
        'jobID': 1,
        'title': 'Software Engineer',
        'description': 'Develops information systems by designing, developing, and installing software solutions.',
        'category': 'Information Technology',
        'applicants_count': 10,
        'years_of_experience': 2,
        'work_arrangement': 'Full Time',
        'location': 'Cairo',
        'salary': 10000,
        'date_posted': '2021-01-01',
        'level': 'Entry Level',


    }
    return render(request, 'status.html', context)

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
            context = {
                'background_image': background_images.objects.first().homepage,
            }
            return redirect('home') 
            
        else:
            # Check if username or password is invalid
            try:
                user = candidate.objects.get(username=username)
                if password != user.password:
                    messages.error(request, 'Invalid Password')
                else:
                    messages.error(request, 'User does not exist')
            except candidate.DoesNotExist:
                messages.error(request, 'User does not exist')            
    return render(request, 'Login.html')

def signout(request):
    logout(request)
    background_image = background_images.objects.first().homepage
    context = {
        'background_image': background_image
    }
    return redirect('home') 

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
        vuniversity = request.POST.get('University')
        vexperience = request.POST.get('Education')
        vsskills = request.POST.get('Sskill')
        vtskills = request.POST.get('Tskill')
        vwork_experience = request.POST.get('Work_experience')
        vlinkedin = request.POST.get('Acc')
        vmajor = request.POST.get('Major')
        vextracurricular = request.POST.get('Extracurricular')
        vjob = job.objects.get( jobID = vjobid)
        vdep = department.objects.get(depID = vjob.depID_id)
        vage = age_calculator(vdob)
        vtitle=vjob.title
        vjob.applicants_count = vjob.applicants_count + 1
        vjob.save()
        data = {
            'First Name': vfname,
            'Last Name': vlname,
            'Address': vaddress,
            'Email': vemail,
            'Military Status': vmilitary_status,
            'Phone': vphone,
            'Date of Birth': vdob,
            'Age': vage,
            'University': vuniversity,
            'Experience': vexperience,
            'Soft Skills': vsskills,
            'Tech Skills': vtskills,
            'Major': vmajor,
            'Work Experience': vwork_experience,
            'Extracurricular Activities': vextracurricular,
            'LinkedIn': vlinkedin,
        }

        # Save data to the 'resume' model
        pdf_filename = create_pdf(data)
        res = resume(pdf_file=pdf_filename,University=vuniversity, Major=vmajor, Education=vexperience, LinkedIn=vlinkedin, Work_Experience=vwork_experience, SoftSkill=vsskills, TechSkill=vtskills, ExtraCurricular=vextracurricular)
        res.save()

        cand = candidate(auto_resume=pdf_filename, cv=vcv, fname=vfname, lname=vlname, jobID=vjob, depID=vdep, phone=vphone, address=vaddress, dob=vdob, military_status=vmilitary_status, email=vemail, age=vage,title=vtitle)
        cand.save()


    background_image = background_images.objects.first().thank_you
    context = {
        'background_image': background_image
    }
    return render(request, 'thankyou.html', context)

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


def CG(request): #TUTORIAL
    background_image = background_images.objects.first().homepage
    context = {
        'background_image': background_image
    }
    return render(request, 'CG.html', context)

@login_required
def Viewstatus(request): 
    # get the current user
    user = request.user
    # get the candidate object of the current user
    cand = candidate.objects.get(email=user.email)
    # get the job object of the candidate
    jobx = job.objects.get(jobID=cand.jobID_id)
    status = cand.cand_status
    message = cand.To_Candidate
    fname = cand.fname
    lname = cand.lname
    email = cand.email
    address = cand.address
    military_status = cand.military_status
    phone = cand.phone
    dob = cand.dob
    age = cand.age
    cv = cand.cv

    context = {
        'background_image': background_images.objects.first().account,
        'status': status,
        'message': message,
        'fname': fname,
        'lname': lname,
        'email': email,
        'address': address,
        'military_status': military_status,
        'phone': phone,
        'dob': dob,
        'age': age,
        'cv': cv,
        'jobID': jobx.jobID,
        'title': jobx.title,
        'description': jobx.description,
        'category': jobx.depID.depName,
        'applicants_count': jobx.applicants_count,
        'years_of_experience': jobx.years_of_experience,
        'work_arrangement': jobx.work_arrangement,
        'location': jobx.location,
        'salary': jobx.salary,
        'date_posted': jobx.date_posted.strftime('%Y-%m-%d'),
        'level': jobx.level,
    }
    return render(request,'status.html', context)


def create_pdf(data):
    pdf_filename = f'{data["First Name"]}_resume.pdf'
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', pdf_filename)

    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    custom_style = ParagraphStyle(name='CustomNormal', parent=styles['Normal'], fontSize=14)
    story.append(Paragraph('Resume Details', styles['Title']))
    story.append(Spacer(1, 12))

    for field, value in data.items():
        story.append(Paragraph(f'<b>{field}:</b> {value}', custom_style))
        story.append(Spacer(1, 10))

    doc.build(story)

    return pdf_file_path

def CV_pdf(request):
    if request.method == 'POST':
        vuniversity = request.POST.get('University')
        vexperience = request.POST.get('Education')
        vsskills = request.POST.get('Sskill')
        vtskills = request.POST.get('Tskill')
        vwork_experience = request.POST.get('Work_experience')
        vlinkedin = request.POST.get('Acc')
        vmajor = request.POST.get('Major')
        vextracurricular = request.POST.get('Extracurricular')

        data = {
            'University': vuniversity,
            'Experience': vexperience,
            'Soft Skills': vsskills,
            'Tech Skills': vtskills,
            'Major': vmajor,
            'Work Experience': vwork_experience,
            'Extracurricular Activities': vextracurricular,
            'LinkedIn': vlinkedin,
        }

        # Save data to the 'resume' model
        pdf_filename = create_pdf(data)
        res = resume(pdf_file=pdf_filename,University=vuniversity, Major=vmajor, Education=vexperience, LinkedIn=vlinkedin, Work_Experience=vwork_experience, SoftSkill=vsskills, TechSkill=vtskills, ExtraCurricular=vextracurricular)
        res.save()
        messages.success(request, 'Resume submitted successfully.')
        return render(request, 'thankyou.html')  # Replace with your success page URL
    return render(request, 'CG.html')  # Replace with your template name
