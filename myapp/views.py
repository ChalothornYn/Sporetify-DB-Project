from django.shortcuts import render, redirect
from .models import *
from .forms import addSongForm
from django.contrib import messages

# Create your views here.
def landingPage(request):
    return render(request, 'index.html', {'field': 20})

def Login(request):
    return render(request, 'login.html')

def Signup(request):
    return render(request, 'signup.html')

def SignupEn(request):
    return render(request, 'signupen.html')

def home(request):
    return render(request, 'layout_role.html')

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
                print([genre1,genre2,genre3])
                print(set([genre1,genre2,genre3]))
                messages.success(request, ('There are duplicate genre (Select none for unselect)'))
        
        if len(language) > 2:
            messages.success(request, ('Song language must be selected'))

        # print()
        
        # print(songImg)
        # print(normalURL)
        # print(goodURL)
        # print(genre1)
        # print(genre2)
        # print(genre3)
        # print(album)
        # print(lyrics)
        # print(description)
        # print(language)


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

def songHome(request):
    return render(request, 'songHome.html')
    
def userProfile(request):
    return render(request, 'userProfile.html')

def adminProfile(request):
    return render(request, 'adminProfile.html')

def songTest(request):
    return render(request, 'layout_song.html')

def songEDM(request):
    return render(request, 'songEDM.html')

def userProfile_edit(request):
    return render(request, 'userProfile_edit.html')

def userProfile_package(request):
    return render(request, 'userProfile_package.html')

def userProfile_transaction(request):
    return render(request, 'userProfile_transaction.html')