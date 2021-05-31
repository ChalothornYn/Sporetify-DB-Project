from django.shortcuts import render

# Create your views here.
def landingPage(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

<<<<<<< HEAD
def addSong(request):
    return render(request, 'addSong.html')
=======
def home(request):
    return render(request, 'layout_role.html')
>>>>>>> 9ffbfd51d871fa4bf544952e66f395ab283a8bd0
