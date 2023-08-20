from django.contrib import admin
from .models import candidate, human_resources, job, candidate_account, department

# Register your models here.

admin.site.site_header = "Admin Panel"
admin.site.site_title = "HR Admin Panel"


@admin.register(human_resources) 
class human_resources(admin.ModelAdmin):
    pass

@admin.register(job)
class JobAdmin(admin.ModelAdmin):
    fields=('title','description','depID','HR_code')
    list_display = ('title','description','depID')
    

"""@admin.register(candidate_account)
class CandidateAccountAdmin(admin.ModelAdmin):
   fields=('candID','username','password')
   list_display=('username','password','candID')
   """

@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    """pass"""
    fields=('depName',)
    list_display=('depName',)
    


@admin.register(candidate)
class candAdmin(admin.ModelAdmin):
    fields = ('cv','fname','address','military_status','phone','dob','cand_status')
    list_display = ('fname','military_status','cv','cand_status')  #to display column 
    list_display_links=('fname',)
    list_editable=('cand_status',)  
    list_filter=('cand_status',)
    search_fields=('fname','dob')
    


  
