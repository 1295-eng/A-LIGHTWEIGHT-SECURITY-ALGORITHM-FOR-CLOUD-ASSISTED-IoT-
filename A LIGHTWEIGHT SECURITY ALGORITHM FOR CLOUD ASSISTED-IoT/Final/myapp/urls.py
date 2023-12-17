from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logou/',views.logou,name='logou'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('enquire/',views.enquire,name='enquire'),
    path('docreg/',views.docreg,name='docreg'),
    path('patientreg/',views.patientreg,name='patientreg'),
    path('welcome/',views.welcome,name='welcome'),
    path('requir/<str:s>',views.requir,name='requir')
    
]
