from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import thingspeak
import json
import math

def home(request):
    return render(request,'home.html')

def register(request):
    '''
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        #if form.is_valid():
        #    form.save()
        #    username = form.cleaned_data.get('username')
        #    password = form.cleaned_data.get('password1')
            username = request.POST['username']
            phone = request.POST['phone']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password==confirm_password:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
            #user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
        '''
    return render(request, 'register.html') 



def login_view(request):
    if request.method == 'POST':
        #form = LoginForm(request.POST)
        #if form.is_valid():
        #    username = form.cleaned_data['username']
        #    password = form.cleaned_data['password']
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                print('l')
                login(request, user)
                return redirect('home')
            else:
                 return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logou(request):
     logout(request)
     return redirect('home')

def about(request):
    return render(request,'about.html')

'''def contact(request):
    if request.method=="POST":
         name = request.POST['name']
         email = request.POST['email']
         message = request.POST['message']
         Contact(name=name,email=email,message=message).save()
    return render(request,'contact.html')'''

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        subject = f'Message from {name}'
        message = f'''Email:  {email} 
        {message}'''
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['19jg1a0528.bhavani@gvpcew.ac.in']
        send_mail( subject, message, email_from, recipient_list )
        messages.info(request,'Message sent!!!')
        return render(request,'contact.html')
    return render(request,'contact.html')

def enquire(request):
     msgs = Contact.objects.all()
     return render(request,'enquire.html',{'msgs':msgs})

def docreg(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        #if form.is_valid():
        #    form.save()
        #    username = form.cleaned_data.get('username')
        #    password = form.cleaned_data.get('password1')
            username = request.POST['username']
            phone = request.POST['phone']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password==confirm_password:
                user = User.objects.create_superuser(username=username,password=make_password(password),email=email, is_staff=True, is_superuser=True)
               
                #User.objects.create_superuser
                user.save()
                return redirect('login')
            #user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('docreg')
    else:
        form = UserCreationForm()
    return render(request, 'docreg.html', {'form': form})

def patientreg(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        #if form.is_valid():
        #    form.save()
        #    username = form.cleaned_data.get('username')
        #    password = form.cleaned_data.get('password1')
            username = request.POST['username']
            phone = request.POST['phone']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password==confirm_password:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
            #user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('patientreg')
    else:
        form = UserCreationForm()
    return render(request, 'patientreg.html', {'form': form})

'''
def doctor_registration(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            doctor = form.save(using='doctor')
            # Do something else, such as redirect to the doctor's profile page
    else:
        form = DoctorRegistrationForm()
    return render(request, 'docreg.html', {'form': form})


def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(using='patient')
            # Do something else, such as redirect to the patient's profile page
    else:
        form = PatientRegistrationForm()
    return render(request, 'patientreg.html', {'form': form})'''




from django.shortcuts import render

import json
import thingspeak
from django.shortcuts import render

def requir(request,s):
     res = Pulse.objects.filter(name=s)
     return render(request,'requir.html',{'res':res,'s':s})

def welcome(request):
    # Retrieve the last field value from ThingSpeak
    username = request.user.username
    if request.user.is_staff:
        k = User.objects.all()
        l = []
        for i in k:
             if i.is_staff==False:
                  l.append(i)
        print(l)
        return render(request,'welcome.html',{'l':l})
    '''
    if username=="Dhanusha":
         ch = thingspeak.Channel(2064440)
    elif username=="Anjali":
         ch = thingspeak.Channel(2064446)
    elif username=="Laya":
         ch = thingspeak.Channel(2064438)
    else:
         ch = thingspeak.Channel(2048186)
    '''
    ch = thingspeak.Channel(2064438)
    r = ch.get({'results':2})
    r = json.loads(r)
    field_value = float(r["feeds"][0]["field1"])
    #decrypted_pulse_data = math.ceil(field_value * 17 / 3233)
    decrypted_pulse_data = field_value
    print(decrypted_pulse_data)
    k = Pulse.objects.last()
    print(k.pul)
    if Pulse.objects.last().pul!=decrypted_pulse_data:
        Pulse(name=username,pul=int(decrypted_pulse_data)).save()
    res = Pulse.objects.filter(name=username)
    context = {'username': username, 'decrypted_pulse_data': decrypted_pulse_data,'res':res}
    return render(request, 'welcome.html', context)
    





