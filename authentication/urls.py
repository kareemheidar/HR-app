from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('addCand', views.addCand, name='addCand'),
    path('jobs', views.jobs, name='jobs'),
    path('application', views.application, name='application'),
    path('apply', views.apply, name='apply'),
    path('get_job/<int:job_id>/', views.get_job_by_id, name='get_job_by_id'),
    path('aboutus', views.aboutus, name='aboutus'),
    #path('get_status', views.get_status, name='get_status'),
    path('forget', views.forgetpassword, name='forget'),
    path('temp', views.temp, name='temp'),
    #path('CV_Generator',views.CV_Generator,name='CV_Generator'),
    path('status',views.Viewstatus,name='status'),
    path('CGT',views.CG,name='CGT'), #TUTORIAL
    path('CV_pdf',views.CV_pdf,name='CV_pdf'),
    # path('venue_pdf', views.venue_pdf,name='venue_pdf')
]
