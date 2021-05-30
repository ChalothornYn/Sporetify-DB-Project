from django.shortcuts import render

# Create your views here.
def hello(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def Signup(request):
    return render(request, 'signup.html')