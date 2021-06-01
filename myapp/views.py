from django.shortcuts import render
from .models import *
from .forms import addSongForm


# Create your views here.
def landingPage(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def Signup(request):
    return render(request, 'signup.html')

def SignupEn(request):
    return render(request, 'signupen.html')

def home(request):
    return render(request, 'layout_role.html')

def addSong(request):
    return render(request, 'addSong.html')

def addSongSubmit(request):
    form = addSongForm()
    if request.method == 'POST':
        form = addSongForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            print('success')
        else:
            print('not success')
    return render(request, 'tempResult.html')
    
def user_profile(request):
    return render(request, 'userProfile.html')
