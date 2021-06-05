from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages

# For authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *

# Create your views here.
def landingPage(request):
    # Force logout before login
    logout(request)
    return render(request, 'index.html')


def playSong(request):
    return render(request, 'playSong.html')

def addSong(request):
    form = addSongForm()
    if request.method == 'POST':
        form = addSongForm(request.POST or None, request.FILES or None)

        songName = request.POST['songName']
        artistID = request.POST['artistID']
        songImg = request.FILES.get('songImg')
        normalURL = request.FILES.get('normalURL')
        goodURL = request.FILES.get('goodURL')
        genre1 = request.POST['genre1']
        genre2 = request.POST['genre2']
        genre3 = request.POST['genre3']
        album = request.POST['album']
        lyrics = request.POST['lyrics']
        description = request.POST['description']
        language = request.POST['language']

        if songName == '':
            messages.success(request, ('Please provide song name'))
        elif len(songName) > 100:
            messages.success(request, ('Your song name cannot exceed 100 character'))

        if artistID == '':
            messages.success(request, ('Please provide artistID'))
        elif len(songName) > 6:
            messages.success(request, ('artistId not found'))
        elif artistID != Artist.objects.get(artistID = artistID):
            messages.success(request, ('artistId not found'))
        
        if songImg == None:
            messages.success(request, ('Please upload song cover image'))
        
        if normalURL == None:
            messages.success(request, ('Please upload normal quality song'))
        
        if goodURL == None:
            messages.success(request, ('Please upload good quality song'))

        if genre1 == 'none':
            messages.success(request, ('Genre 1 must be selected'))
        elif genre2 != 'none' or genre3 != 'none':
            if len([genre1,genre2,genre3]) != len(set([genre1,genre2,genre3])):
                messages.success(request, ('There are duplicate genre (Select none for unselect)'))
        
        if len(language) > 2:
            messages.success(request, ('Song language must be selected'))

        # Is form valid?
        if form.is_valid():
            form.save()
            print('success')
            result = Song.objects.last()
            return render(request, 'tempResult.html', {'result': result})
        else:
            print(form.errors)
            print('not success')
            return render(request, 'addSong.html', {'form': form})
    else:
        return render(request, 'addSong.html')


def addSongSubmit(request):
    form = addSongForm()
    if request.method == 'POST':
        form = addSongForm(request.POST or None, request.FILES or None)
        #fields = ['songName', 'artistID', 'songImg', 'normalURL', 'goodURL', 'genre1', 'genre2', 'genre3', 'album', 'lyrics', 'description', 'language'] 
        songName = request.POST['songName']
        artistID = request.POST['artistID']
        songImg = request.POST['songImg']
        normalURL = request.POST['normalURL']
        goodURL = request.POST['goodURL']
        genre1 = request.POST['genre1']
        genre2 = request.POST['genre2']
        genre3 = request.POST['genre3']
        album = request.POST['album']
        lyrics = request.POST['lyrics']
        description = request.POST['description']
        language = request.POST['language']

        if form.is_valid():
            form.save()
            print('success')
            result = Song.objects.last()
            return render(request, 'tempResult.html', {'result': result})
        else:
            print(form.errors)
            print('not success')

    return render(request, 'tempResult.html')
    
def Testtable(request):
    return render(request, 'testtable.html')

def AdminHistory(request):
    return render(request, 'history.html')

# ------------------------------------------- Song views -------------------------------------------

def songHome(request):
    return render(request, 'songHome.html')
    
def userProfile(request):
    return render(request, 'userProfile.html')

def songTest(request):
    return render(request, 'layout_song.html')

def songEDM(request):
    return render(request, 'songEDM.html')

# ------------------------------------------- User views -------------------------------------------
# Customer Register Page
@unauthenticated_customer
def signupUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        form = addCustomer(request.POST)

        context = {'username':username, 'email':email, 'form':form}
        if form.is_valid():
            customerUser = form.save()

            # Add admin role to user
            group = Group.objects.get(name='customer')
            customerUser.groups.add(group)

            # Create OneToOne relationship to user  
            Customer.objects.create(user=customerUser,)
            print('success')
            return redirect('login')
        else:
            # Form is not valid
            print(form.errors)
            return render(request, 'signup.html', context)
    return render(request, 'signup.html')

# Customer login Page
@unauthenticated_customer
def loginUser(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/userprofile/')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'login.html', {'username':username})
    return render(request, 'login.html')

# Customer Profile Page
@login_required(login_url='enLogin')
@customer_only
def userProfile(request):
    return render(request, 'userProfile.html')

def userProfile_edit(request):
    return render(request, 'userProfile_edit.html')

def userProfile_package(request):
    return render(request, 'userProfile_package.html')

def userProfile_transaction(request):
    return render(request, 'userProfile_transaction.html')

def userProfile_family(request):
    return render(request, 'userProfile_family.html')


# --------------------------------------- Entertainmemt views -------------------------------------
# Entertainment Register Page
@unauthenticated_entertainment
def signupEntertainment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        form = addEntertainment(request.POST)

        context = {'username':username, 'email':email, 'form':form}
        if form.is_valid():
            entertainmentUser = form.save()

            # Add admin role to user
            group = Group.objects.get(name='entertainment')
            entertainmentUser.groups.add(group)

            # Create OneToOne relationship to user  
            Entertainment.objects.create(user=entertainmentUser,)
            print('success')
            return redirect('enLogin')
        else:
            # Form is not valid
            print(form.errors)
            return render(request, 'entertainmentPages/signupEntertainment.html', context)
    return render(request, 'entertainmentPages/signupEntertainment.html')

# Entertainment Login Page
@unauthenticated_entertainment
def loginEntertainment(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('enDashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'entertainmentPages/loginEntertainment.html', {'username':username})
    return render(request, 'entertainmentPages/loginEntertainment.html')

# Entertainment Dashboard Page
@login_required(login_url='enLogin')
@entertainment_only
def enDashboard(request):
    return render(request, 'entertainmentPages/enDashboard.html')


# ------------------------------------------- Admin views -----------------------------------------

# Admin Register Page
@unauthenticated_admin
def adminRegister(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        form = addAdmin(request.POST)

        context = {'username':username, 'email':email, 'form':form}
        if form.is_valid():
            adminUser = form.save()

            # Add admin role to user
            group = Group.objects.get(name='admin')
            adminUser.groups.add(group)

            # Create OneToOne relationship to user  
            Admin.objects.create(user=adminUser,)
            print('success')
            return redirect('adminLogin')
        else:
            # Form is not valid
            print(form.errors)
            return render(request, 'adminPages/adminRegister.html', context)
    return render(request, 'adminPages/adminRegister.html')

# Admin Login Page
@unauthenticated_admin
def adminLogin(request):
    # Force logout before login
    logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('adminProfile')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'adminPages/adminLogin.html', {'username':username})
    return render(request, 'adminPages/adminLogin.html')

# Admin Logout fn
def adminLogout(request):
    logout(request)
    return redirect('adminLogin')

# Admin Profile Page
@login_required(login_url='adminLogin')
@admin_only
def adminProfile(request):
    return render(request, 'adminPages/adminProfile.html')
