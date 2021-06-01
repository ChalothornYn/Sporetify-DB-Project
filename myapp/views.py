from django.shortcuts import render

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
    Sname = request.POST['Sname']
    Aname = request.POST['Aname']
    return render(request, 'tempResult.html', {'Sname': Sname, 'Aname': Aname})