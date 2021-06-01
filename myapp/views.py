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