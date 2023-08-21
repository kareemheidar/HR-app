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
    #path('get_status', views.get_status, name='get_status')
]
