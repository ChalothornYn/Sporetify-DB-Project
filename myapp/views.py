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
        form = addSongForm(request.POST or None, request.FILES or None)
        print(form.errors)
        if form.is_valid():
            form.save()
            print('success')
        else:
            print('not success')
    result = Song.objects.last()
    return render(request, 'tempResult.html', {'result': result})
    
def Testtable(request):
    return render(request, 'testtable.html')

def AdminHistory(request):
    return render(request, 'adminhistory.html')

def songHome(request):
    return render(request, 'songHome.html')
    
def userProfile(request):
    return render(request, 'userProfile.html')

def songTest(request):
    return render(request, 'layout_song.html')

def songEDM(request):
    return render(request, 'songEDM.html')