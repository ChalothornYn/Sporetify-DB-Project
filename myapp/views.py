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


def home(request):
    return render(request, 'layout_role.html')
