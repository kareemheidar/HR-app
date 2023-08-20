from django.contrib import admin
from .models import candidate, human_resources, job, candidate_account, department, background_images
from django.contrib.auth.models import User
from django.contrib import messages

# Register your models here.

admin.site.site_header = "Admin Panel"
admin.site.site_title = "HR Admin Panel"

def register_candidate(modeladmin, request, queryset): #to allow candidate to login - an action is created to transfer candidate data in user.auth
    for candidate in queryset:
        if candidate.username is not None and candidate.password is not None:
            username = candidate.username
            password = candidate.password
            email = candidate.email
            newuser = User.objects.create_user(username, email, password)
            newuser.first_name = candidate.fname
            newuser.last_name = candidate.lname
            newuser.save()
        else:
            messages.error(request, 'Insert Username & Password')


@admin.register(human_resources) 
class human_resources(admin.ModelAdmin):
    pass

@admin.register(job)
class JobAdmin(admin.ModelAdmin):
    fields=('title','description','depName','depID','HR_code','applicants_count','level','work_arrangement','salary', 'years_of_experience', 'location')
    list_display = ('title', 'depName','applicants_count')
    

@admin.register(candidate_account)
class CandidateAccountAdmin(admin.ModelAdmin):
    fields=('username','password','candID.email')
    list_display = ('username', 'candID')
    actions = [register_candidate]

@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    fields=('depName',)
    list_display=('depName',)
    
@admin.register(background_images)
class BackgroundImagesAdmin(admin.ModelAdmin):
    fields=('homepage','jobs','application','thank_you','logout','login','account')
    list_display=('homepage','jobs','application','thank_you','logout','login','account')

@admin.register(candidate)
class candAdmin(admin.ModelAdmin):
    fields = ('cv','fname','address','military_status','phone','dob','cand_status','email','jobID','password', 'username', 'age')
    list_display = ('fname','cv','cand_status',)  #to display column 
    list_display_links=('fname',)
    list_editable=('cand_status',)  
    list_filter=('cand_status',)
    search_fields=('fname','dob')
    actions = [register_candidate]

    


  
