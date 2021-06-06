from django.db import reset_queries
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from datetime import date, datetime

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

def viewSong(request):
    return render(request, 'song.html')


def playSong(request):
    return render(request, 'playSong.html')
def Songtestjs(request):
    return render(request, 'songtestjs.html')


# def addSong(request):
#     form = addSongForm()
#     if request.method == 'POST':
#         form = addSongForm(request.POST or None, request.FILES or None)

#         songName = request.POST['songName']
#         artistID = request.POST['artistID']
#         songImg = request.FILES.get('songImg')
#         normalURL = request.FILES.get('normalURL')
#         goodURL = request.FILES.get('goodURL')
#         genre1 = request.POST['genre1']
#         genre2 = request.POST['genre2']
#         genre3 = request.POST['genre3']
#         album = request.POST['album']
#         lyrics = request.POST['lyrics']
#         description = request.POST['description']
#         language = request.POST['language']

#         if songName == '':
#             messages.success(request, ('Please provide song name'))
#         elif len(songName) > 100:
#             messages.success(request, ('Your song name cannot exceed 100 character'))

#         if artistID == '':
#             messages.success(request, ('Please provide artistID'))
#         elif len(songName) > 6:
#             messages.success(request, ('artistId not found'))
#         elif artistID != Artist.objects.get(artistID = artistID):
#             messages.success(request, ('artistId not found'))
        
#         if songImg == None:
#             messages.success(request, ('Please upload song cover image'))
        
#         if normalURL == None:
#             messages.success(request, ('Please upload normal quality song'))
        
#         if goodURL == None:
#             messages.success(request, ('Please upload good quality song'))

#         if genre1 == 'none':
#             messages.success(request, ('Genre 1 must be selected'))
#         elif genre2 != 'none' or genre3 != 'none':
#             if len([genre1,genre2,genre3]) != len(set([genre1,genre2,genre3])):
#                 messages.success(request, ('There are duplicate genre (Select none for unselect)'))
        
#         if len(language) > 2:
#             messages.success(request, ('Song language must be selected'))

#         # Is form valid?
#         if form.is_valid():
#             form.save()
#             print('success')
#             result = Song.objects.last()
#             return render(request, 'tempResult.html', {'result': result})
#         else:
#             print(form.errors)
#             print('not success')
#             return render(request, 'addSong.html', {'form': form})
#     else:
#         return render(request, 'addSong.html')


def addSong(request):
    form = addSongForm()
    if request.method == 'POST':
        errorFlag = 0
        form = addSongForm(request.POST or None, request.FILES or None)

        songName = request.POST['songName']
        artistID = request.POST['artistID']
        album = request.POST['album']
        songImg = request.FILES.get('songImg')
        normalURL = request.FILES.get('normalURL')
        goodURL = request.FILES.get('goodURL')
        genre1 = request.POST['genre1']
        genre2 = request.POST['genre2']
        genre3 = request.POST['genre3']
        language = request.POST['language']
        lyrics = request.POST['lyrics']
        description = request.POST['description']

        if songName == '':
            messages.success(request, ('Please provide song name'))
            errorFlag = 1
        elif len(songName) > 100:
            messages.success(request, ('Your song name cannot exceed 100 character'))
            errorFlag = 1

        if artistID == '':
            messages.success(request, ('Please provide artist ID'))
            errorFlag = 1
        elif len(artistID) > 8:
            messages.success(request, ('artist ID not found'))
            errorFlag = 1
        elif not ((request.user.artist_set.filter(artistID = artistID)).exists()):
            messages.success(request, ('artist ID not found'))
            errorFlag = 1
        
        if genre1 == 'none':
            messages.success(request, ('Genre 1 must be selected'))
            errorFlag = 1
        elif genre2 != 'none' or genre3 != 'none':
            if len([genre1,genre2,genre3]) != len(set([genre1,genre2,genre3])):
                messages.success(request, ('There are duplicate genre (Select none for unselect)'))
                errorFlag = 1

        if songImg == None:
            messages.success(request, ('Please upload song cover image'))
            errorFlag = 1
        
        if normalURL == None:
            messages.success(request, ('Please upload normal quality song'))
            errorFlag = 1
        
        if goodURL == None:
            messages.success(request, ('Please upload good quality song'))
            errorFlag = 1
        
        if len(language) > 2:
            messages.success(request, ('Song language must be selected'))
            errorFlag = 1

        context = {'songName': songName, 
                    'artistID': artistID, 
                    'album': album,
                    'lyrics': lyrics,
                    'description': description}

        # Is form valid?
        if errorFlag == 0:
            if form.is_valid():
                form.save()
                print('success')
                if request.user.groups.all()[0].name == 'entertainment':
                    return redirect('enDashboard')
                if request.user.groups.all()[0].name == 'admin':
                    return redirect('adminProfile')
        print(form.errors)
        print('not success')
        return render(request, 'songPages/addSong.html', context)
    else:
        return render(request, 'songPages/addSong.html')

# def addSongSubmit(request):
#     form = addSongForm()
#     if request.method == 'POST':
#         form = addSongForm(request.POST or None, request.FILES or None)
#         #fields = ['songName', 'artistID', 'songImg', 'normalURL', 'goodURL', 'genre1', 'genre2', 'genre3', 'album', 'lyrics', 'description', 'language'] 
#         songName = request.POST['songName']
#         artistID = request.POST['artistID']
#         songImg = request.POST['songImg']
#         normalURL = request.POST['normalURL']
#         goodURL = request.POST['goodURL']
#         genre1 = request.POST['genre1']
#         genre2 = request.POST['genre2']
#         genre3 = request.POST['genre3']
#         album = request.POST['album']
#         lyrics = request.POST['lyrics']
#         description = request.POST['description']
#         language = request.POST['language']

#         if form.is_valid():
#             form.save()
#             print('success')
#             result = Song.objects.last()
#             return render(request, 'tempResult.html', {'result': result})
#         else:
#             print(form.errors)
#             print('not success')

#     return render(request, 'tempResult.html')
    
def Testtable(request):
    return render(request, 'testtable.html')

def AdminHistory(request):
    return render(request, 'history.html')

# ------------------------------------------- Song views -------------------------------------------

def songHome(request):
    return render(request, 'songHome.html')

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

        if (user is not None) and (user.groups.all()[0].name == 'customer'):
            login(request, user)
            return redirect('/userprofile/')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'login.html', {'username':username})
    return render(request, 'login.html')

def usersongHistory(request):
    return render(request, 'usersongHistory.html')

# ------------------------------------------- Customer profile -------------------------------------------
@login_required(login_url='enLogin')
@customer_only
# Account overview
def userProfile(request):
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    # calculate age
    if customer.dob != None:
        birth = customer.dob
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    else:
        age = None
    # full gender
    gender = {
        None: None,
        'M': 'Male',
        'F': 'Female',
        'O': 'Non-binary'
    }
    # phone number
    phone = customer.interCode + ' ' + customer.telNO if customer.interCode != None and customer.telNO != None else None

    # sending data to html
    send_data = {
        'user': user, 
        'customer': customer, 
        'age': age,
        'gender': gender[customer.gender],
        'phone': phone
    }
    return render(request, 'userProfile.html', send_data)

# Edit profile
def userProfile_edit(request):
    ### show result ###
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    # date of birth
    DOB = str(datetime.strptime(str(customer.dob), '%Y-%m-%d').date()) if customer.dob != None else None
    #phone
    telNO = customer.interCode + customer.telNO if customer.telNO != None and customer.interCode != None else ''

    ### update ###
    form = editCusInfo(instance=customer)
    if request.method == 'POST':
        form = editCusInfo(request.POST or None, request.FILES or None, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/userprofile/edit')
    
    # sending data to html
    send_data = {
        'user': user, 
        'customer': customer,
        'DOB': DOB,
        'telNO': telNO,
        'form': form
    }
    return render(request, 'userProfile_edit.html', send_data)

# Customer package
def userProfile_package(request):
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    package = Package.objects.get(packageID=customer.packageID_id)

    ### update ###
    form = packCusInfo(instance=customer)
    if request.method == 'POST':
        form = packCusInfo(request.POST or None, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/userprofile/package')

    # sending data to html
    send_data = {
        'user': user, 
        'customer': customer, 
        'package': package
    }

    return render(request, 'userProfile_package.html', send_data)

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

        if (user is not None) and (user.groups.all()[0].name == 'entertainment'):
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
    allArtist = Artist.objects.filter(entertainmentID = request.user.id)
    # latest5Artist = request.user.artist_set.all().order_by('-artistID')[:5]
    Qlatest5Artist = allArtist.order_by('-artistID')[:5]
    artist_count = request.user.artist_set.count()

    latest5Artist = [None, None, None, None, None]
    latest5Song = [None, None, None, None, None]
    index = 0
    song_count = 0

    allSong = Song.objects.all().order_by('-songID')
    for song in allSong:
        # print(song.artistID.artistID)
        if request.user.artist_set.filter(artistID = song.artistID.artistID).exists():
            song_count = song_count + 1
            if index < 5:
                latest5Song[index] = song
            index = index + 1

    for x in range(5):
        if x < len(Qlatest5Artist):
            latest5Artist[x] = Qlatest5Artist[x]
        else:
            latest5Artist[x] = None

    # print(latest5Artist)
    # print(latest5Artist[0].artistName)

    # if request.user.groups.all()[0].name == 'entertainment':
    #     userROLE[0] = None
    # if request.user.groups.all()[0].name == 'admin':
    #     userROLE[0] = 1
    print(artist_count)
    print(song_count)
    print(latest5Artist[0].profileImage.url)

    context = {'latest5Artist': latest5Artist, 'latest5Song': latest5Song,
                'artistPresent':latest5Artist[0],
                'songPresent':latest5Song[0],
                'song_count': song_count,
                'artist_count':artist_count,}

    return render(request, 'entertainmentPages/enDashboard.html', context)

def songHistoryforEntertainment(request):
    return render(request, 'entertainmentPages/songHistoryforEntertainment.html')

def enProfile (request):
    context = {}
    return render(request, 'entertainmentPages/enProfile.html', context)

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

        if (user is not None) and (user.groups.all()[0].name == 'admin'):
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


#  ------------------------------ Artist ------------------------------------

def addArtist(request):
    form = addArtistForm()
    if request.method == 'POST':
        form = addArtistForm(request.POST or None, request.FILES or None)

        artistName = request.POST.get('artistName')
        profileImage = request.FILES.get('profileImage')
        dob = request.POST.get('dob')
        
        context = {'artistName':artistName, 'dob':dob}

        # Is form valid?
        if form.is_valid():
            # ----------- Add FK autometically -----------
            addArtistFK = form.save(commit=False)
            addArtistFK.entertainmentID = request.user
            addArtistFK.save()
            print('success')
            if request.user.groups.all()[0].name == 'entertainment':
                return redirect('enDashboard')
            if request.user.groups.all()[0].name == 'admin':
                return redirect('adminProfile')
            return redirect('enDashboard')
        else:
            print(form.errors)
            print('not success')
            return render(request, 'artistPages/addArtist.html', context)
    else:
        return render(request, 'artistPages/addArtist.html')

def showAllArtist (request):
    # print('here')
    context = {'artists': request.user.artist_set.all().order_by('-artistID')}
    # print('here')
    # print(request.user.artist_set.all().order_by('-artistID'))
    # context = {}
    return render(request, 'artistPages/allArtistTable.html', context)

def updateArtist(request, pk):
    artist = Artist.objects.get(artistID = pk)
    form = addArtistForm(instance=artist)
    if request.method == 'POST':
        form = addArtistForm(request.POST or None, request.FILES or None, instance=artist)

        # Is form valid?
        if form.is_valid():
            form.save()
            print('success')
            if request.user.groups.all()[0].name == 'entertainment':
                return redirect('enDashboard')
            if request.user.groups.all()[0].name == 'admin':
                return redirect('adminProfile')
        else:
            print(form.errors)
            print('not success')
            return render(request, 'artistPages/updateArtist.html', {'artist': artist})
    else:
        return render(request, 'artistPages/updateArtist.html', {'form': form, 'artist': artist})

def deleteArtist (request, pk):
    artist = Artist.objects.get(artistID = pk)
    artist_song = artist.song_set.count()
    if request.method == 'POST':
        artist.delete()
        if request.user.groups.all()[0].name == 'entertainment':
            return redirect('enDashboard')
        if request.user.groups.all()[0].name == 'admin':
            return redirect('adminProfile')

    context = {'artist': artist, 'count': artist_song}
    return render(request, 'artistPages/deleteArtist.html', context)

def singleArtist(request, pk):
    artist = Artist.objects.get(artistID = pk)
    artist_song = artist.song_set.all()
    count = artist.song_set.count()
    context = {'artist': artist, 'count': count, 'artist_song': artist_song}
    return render(request, 'artistPages/singleArtist.html', context)


#  ------------------------------ Song ------------------------------------

def showAllSong(request):
    songs = []
    index = 0
    song_count = 0
    allSong = Song.objects.all().order_by('-songID')
    for song in allSong:
        # print(song.artistID.artistID)
        if request.user.artist_set.filter(artistID = song.artistID.artistID).exists():
            songs.append(song)
    context = {'songs': songs}

    return render(request, 'songPages/allSongTable.html', context)


def updateSong(request, pk):
    errorFlag = 0
    song = Song.objects.get(songID = pk)
    form = addSongForm(instance=song)

    if request.method == 'POST':
        form = addSongForm(request.POST or None, request.FILES or None, instance=song)

        genre1 = request.POST['genre1']
        genre2 = request.POST['genre2']
        genre3 = request.POST['genre3']

        if genre1 == 'none':
            messages.success(request, ('Genre 1 must be selected'))
            errorFlag = 1
        elif genre2 != 'none' or genre3 != 'none':
            if len([genre1,genre2,genre3]) != len(set([genre1,genre2,genre3])):
                messages.success(request, ('There are duplicate genre (Select none for unselect)'))
                errorFlag = 1


        if errorFlag == 0:
        # Is form valid?
            if form.is_valid():
                form.save()
                print('success')
                if request.user.groups.all()[0].name == 'entertainment':
                    return redirect('enDashboard')
                if request.user.groups.all()[0].name == 'admin':
                    return redirect('adminProfile')
        print(form.errors)
        print('not success')
        return render(request, 'songPages/updateSong.html', {'form': form, 'song': song})
    else:
        # return render(request, 'updateSong.html', {'song': song})
        return render(request, 'songPages/updateSong.html', {'form': form, 'song': song})

def deleteSong (request, pk):
    song = Song.objects.get(songID = pk)
    if request.method == 'POST':
        song.delete()
        if request.user.groups.all()[0].name == 'entertainment':
                return redirect('enDashboard')
        if request.user.groups.all()[0].name == 'admin':
            return redirect('adminProfile')

    context = {'song': song}
    return render(request, 'deleteSong.html', context)

def adminProfile(request):
    return render(request, 'adminPages/adminProfile.html')

def singleSong (request, pk):
    song = Song.objects.get(songID = pk)
    context = {'song': song}
    return render(request, 'songPages/singleSong.html', context)
