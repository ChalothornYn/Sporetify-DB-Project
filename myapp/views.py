from django.shortcuts import render

# Create your views here.
def hello(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def Register(request):
    return render(request, 'register.html')