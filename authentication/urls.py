from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('addCand', views.addCand, name='addCand'),
    path('jobs', views.jobs, name='jobs'),
    path('application', views.application, name='application'),
    path('apply', views.apply, name='apply')
]
