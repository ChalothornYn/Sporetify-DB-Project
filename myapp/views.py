from django.db import reset_queries
from django.db.models.indexes import Index
from django.forms.utils import pretty_name
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from datetime import date, datetime, timedelta

# For authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from json import dumps

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.shortcuts import get_object_or_404

# Create your views here.
def landingPage(request):
    # Force logout before login
    logout(request)
    return render(request, 'index.html')

def viewSong(request):
    # data = ["Laugh"]
    # data = dumps(data)
    songs = Song.objects.all().order_by('-songID')
    context = {'songs': songs}
    return render(request, 'song.html', context)

def playSong(request, pk):
    song = Song.objects.get(songID = pk)
    customer = Customer.objects.get(user_id = request.user)

    form = addListeningHist()
    history = form.save(commit=False)
    history.customerID = customer
    history.songID = song
    history.save()

    context = {'song': song}
    return render(request, 'playSong.html', context)

# def listening(request):
#     return render()

def Songtestjs(request):
    return render(request, 'songtestjs.html')


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
        elif request.user.groups.all()[0].name == 'entertainment':
            # Can add only they own artist
            if not ((request.user.artist_set.filter(artistID = artistID)).exists()):
                messages.success(request, ('artist ID not found'))
                errorFlag = 1
        elif request.user.groups.all()[0].name == 'admin':
            # Can add to any artist
            if not (Artist.objects.filter(artistID = artistID).exists()):
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
                    return redirect('adminDashboard')
        print(form.errors)
        print('not success')
        if request.user.groups.all()[0].name == 'entertainment':
            return render(request, 'songPages/addSong.html', context)
        if request.user.groups.all()[0].name == 'admin':
            return render(request, 'songPages/ADaddSong.html', context)
    else:
        if request.user.groups.all()[0].name == 'entertainment':
            return render(request, 'songPages/addSong.html')
        if request.user.groups.all()[0].name == 'admin':
            return render(request, 'songPages/ADaddSong.html')
    
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
            return redirect('/song')
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
    package = Package.objects.get(packageID=customer.packageID_id)
    
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
    if Family.objects.filter(familyID=customer.familyID_id).exists():
        family = Family.objects.get(familyID=customer.familyID_id)
        childs = Customer.objects.filter(familyID_id = family.familyID).exclude(customerID = family.manager)
        childID = []
        for i in range(len(childs)):
            childID.append(childs[i].user_id)
        childUser = User.objects.filter(customer__user_id__in=childID)    
        manager = Customer.objects.get(customerID = family.manager)
        managerUser = User.objects.get(id=manager.user_id)
        empty_list = '123'[:(3-len(childs))]
        # sending data to html
        send_data = {
            'user': user, 
            'customer': customer, 
            'age': age,
            'gender': gender[customer.gender],
            'phone': phone,
            'package': package,
            'childs': zip(childs, childUser),
            'manager': manager,
            'managerUser': managerUser,
            'empty_list': empty_list
        }
    else:
        send_data = {
            'user': user, 
            'customer': customer, 
            'age': age,
            'gender': gender[customer.gender],
            'phone': phone,
            'package': package,
            'manager': customer,
            'managerUser': user,
            'empty_list': '123'
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
    errorflag = 0
    ### update ###
    if request.method == 'POST':
        # validation
        if request.POST['gender'] == None:
            messages.success(request, ('Gender must be selected'))
            errorflag = 1
            
        if request.POST['dob'] == None:
            messages.success(request, ('Please field your date of birth'))
            errorflag = 1
        
        if request.POST['interCode']== None or request.POST['telNO'] == None:
            messages.success(request, ('Please field your telephone number'))
            errorflag = 1

        if request.POST['firstName'] == "No data":
            messages.success(request, ('Please field your firstname'))
            errorflag = 1
        
        if request.POST['lastName'] == "No data":
            messages.success(request, ('Please field your lastname'))
            errorflag = 1

        if errorflag==0:
            form = editCusInfo(request.POST or None, request.FILES or None, instance=customer)
            if form.is_valid():
                form.save()
        # date of birth
        DOB = str(datetime.strptime(str(customer.dob), '%Y-%m-%d').date()) if customer.dob != None else None
        #phone
        telNO = customer.interCode + customer.telNO if customer.telNO != None and customer.interCode != None else ''
    
    # sending data to html
    send_data = {
        'user': user, 
        'customer': customer,
        'DOB': DOB,
        'telNO': telNO
    }
    return render(request, 'userProfile_edit.html', send_data)

# Customer package
def userProfile_package(request):
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    package = Package.objects.get(packageID=customer.packageID_id)
    if Family.objects.filter(familyID=customer.familyID_id).exists():
        family = Family.objects.get(familyID=customer.familyID_id)
        childs = Customer.objects.filter(familyID_id = family.familyID).exclude(customerID = family.manager)
        
        childID = []
        for i in range(len(childs)):
            childID.append(childs[i].user_id)
        childUser = User.objects.filter(customer__user_id__in=childID)    
        manager = Customer.objects.get(customerID = family.manager)
        managerUser = User.objects.get(id=manager.user_id)
        empty_list = '123'[:(3-len(childs))]
    

    ### update ###
    if request.method == 'POST':
        # Nothing change
        
        # Change group // change packageID, same Family ID, change package to everyone!    ### Please change package to everyone !!!!
        if customer.packageID_id[1] == 'G' and request.POST['packageID'][1] == 'G':
            # change package (for everyone)
            if 'packageID' in request.POST:
                packageIDform = packCusInfo(request.POST or None, instance=customer)
                if packageIDform.is_valid():
                    packageIDform.save()
            

        # Solo -> group // change packageID, add Family, changeFamily only user
        elif customer.packageID_id[1] != 'G' and request.POST['packageID'][1] == 'G':
            # add family
            famID = ""
            if 'manager' in request.POST:
                managerform = addFamily(request.POST or None)
                if managerform.is_valid():
                    famID = managerform.save()
            famID = famID.familyID

            # update familyID
            if 'familyID' in request.POST:
                familyForm = changeFamily(request.POST or None, instance=customer)
                if familyForm.is_valid():
                    new_familyForm = familyForm.save(commit=False)
                    new_familyForm.familyID_id = famID
                    new_familyForm.save()
                    familyForm.save()

            # change package
            if 'packageID' in request.POST:
                packageIDform = packCusInfo(request.POST or None, instance=customer)
                if packageIDform.is_valid():
                    packageIDform.save()
            

        # group -> solo // change packageID, delete Family                              ##### Please update all to None !!!!!!!
        elif customer.packageID_id[1] == 'G' and request.POST['packageID'][1] != 'G':
            # change package
            if 'packageID' in request.POST:
                packageIDform = packCusInfo(request.POST or None, instance=customer)
                if packageIDform.is_valid():
                    packageIDform.save()
            # update familyID to None
            if 'familyID' in request.POST:
                familyForm = changeFamily(request.POST or None, instance=customer)
                if familyForm.is_valid():
                    new_familyForm = familyForm.save(commit=False)
                    new_familyForm.familyID_id = None
                    new_familyForm.save()
                    familyForm.save()

        # solo -> solo // change packageID, not add not change Family
        else:
            #change package
            if 'packageID' in request.POST:
                packageIDform = packCusInfo(request.POST or None, instance=customer)
                if packageIDform.is_valid():
                    packageIDform.save()
        
        user = request.user
        customer = Customer.objects.get(user_id=user.id)
        package = Package.objects.get(packageID=customer.packageID_id)
    if Family.objects.filter(familyID=customer.familyID_id).exists():
        family = Family.objects.get(familyID=customer.familyID_id)
        childs = Customer.objects.filter(familyID_id = family.familyID).exclude(customerID = family.manager)
        childID = []
        for i in range(len(childs)):
            childID.append(childs[i].user_id)
        childUser = User.objects.filter(customer__user_id__in=childID)    
        manager = Customer.objects.get(customerID = family.manager)
        managerUser = User.objects.get(id=manager.user_id)
        empty_list = '123'[:(3-len(childs))]
        if package.packageID[1] == 'F':
            duration = '-'
        elif package.packageID[3] == '1':
            duration = datetime.now() + timedelta(days=30)
        elif package.packageID[3] == '2':
            duration = datetime.now() + timedelta(days=60)
        elif package.packageID[3] == '3':
            duration = datetime.now() + timedelta(days=7)

        # sending data to html
        send_data = {
            'user': user, 
            'customer': customer, 
            'package': package,
            'childs': zip(childs, childUser),
            'manager': manager,
            'managerUser': managerUser,
            'empty_list': empty_list,
            'duration': duration
        }
    else:
        send_data = {
            'user': user, 
            'customer': customer, 
            'manager': customer,
            'managerUser': user,
            'package': package,
            'empty_list': '123'
        }

    return render(request, 'userProfile_package.html', send_data)

# family table
def userProfile_family(request):
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    package = Package.objects.get(packageID=customer.packageID_id)
    if Family.objects.filter(familyID=customer.familyID_id).exists():
        family = Family.objects.get(familyID=customer.familyID_id)
        childs = Customer.objects.filter(familyID_id = family.familyID).exclude(customerID = family.manager)
        
        childID = []
        for i in range(len(childs)):
            childID.append(childs[i].user_id)
        childUser = User.objects.filter(customer__user_id__in=childID)    
        manager = Customer.objects.get(customerID = family.manager)
        managerUser = User.objects.get(id=manager.user_id)
        empty_list = '123'[:(3-len(childs))]

        if request.method == "POST":
            # DELETE member
            if 'delMember' in request.POST:
                if Customer.objects.filter(customerID=request.POST['delMember']).exists():
                    member = Customer.objects.get(customerID=request.POST['delMember'])
                    memberChange = manageFamily(request.POST or None, instance=member)
                    if memberChange.is_valid():
                        del_member = memberChange.save(commit=False)
                        del_member.packageID_id = "PF00"
                        del_member.familyID = None
                        del_member.save()
                        memberChange.save()
                #else:
            # ADD member
            if 'addMember' in request.POST:
                if Customer.objects.filter(customerID=request.POST['addMember']).exists():
                    newMember = Customer.objects.get(customerID=request.POST['addMember'])
                    memberChange = manageFamily(request.POST or None, instance=newMember)
                    if memberChange.is_valid():
                        memberChange.save()
                    else:
                        print("ERROR: ", memberChange.errors)

            if 'manager' in request.POST and 'delMember' not in request.POST:
                new_manager = addFamily(request.POST or None, instance=family)
                if new_manager.is_valid():
                    new_manager.save()
                else:
                    print("ERROR: ", new_manager.errors)

            user = request.user
            customer = Customer.objects.get(user_id=user.id)
            package = Package.objects.get(packageID=customer.packageID_id)
            family = Family.objects.get(familyID=customer.familyID_id)
            childs = Customer.objects.filter(familyID_id = family.familyID).exclude(customerID = family.manager)
            childID = []
            for i in range(len(childs)):
                childID.append(childs[i].user_id)
            childUser = User.objects.filter(customer__user_id__in=childID)
            manager = Customer.objects.get(customerID = family.manager)
            managerUser = User.objects.get(id=manager.user_id)
            empty_list = '123'[:(3-len(childs))]

        # sending data to html
        send_data = {
            'user': user, 
            'customer': customer,
            'childs': zip(childs, childUser),
            'delete': zip(childs, childUser),
            'family': family,
            'manager': manager,
            'managerUser': managerUser,
            'empty_list': empty_list,
            'package': package
        }
    else:
        send_data = {
            'user': user, 
            'customer': customer,
            'manager': customer,
            'managerUser': user,
            'empty_list': '123',
            'package': package
        }
    return render(request, 'userProfile_family.html', send_data)

# Card and Add card
def userProfile_transaction(request):
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    if request.method == "POST":
        if 'number' in request.POST and 'name' in request.POST and 'type' in request.POST and 'expiry' in request.POST and 'cvc' in request.POST:
            if not Card_details.objects.filter(cardID=request.POST['number']).exists():
                card = addCard(request.POST or None)
                if card.is_valid():
                    new_card = card.save(commit=False)
                    new_card.cardID = request.POST['number']
                    new_card.cardType = request.POST['type']
                    expiry = request.POST['expiry']
                    month, year = expiry.split(' / ')
                    new_card.expireDate = year+"-"+month+"-01"
                    new_card.cvv = request.POST['cvc']
                    new_card.save()
                    card.save()

                    collect = request.POST.copy()
                    collect['customer_ID'] = customer.customerID
                    collect['card_ID'] = request.POST['number']
                    if Card.objects.filter(customer_ID = customer.customerID).exists():
                        collect['activate'] = False                     #Case have new card already
                    else:
                        collect['activate'] = True                      #Case this is new card
                    request.POST = collect
                    # create Card table
                    matchCard = collectCard(request.POST or None)
                    if matchCard.is_valid():
                        matchCard.save()
                    else:
                        print("match card ERROR: ", matchCard.errors)

                
                
                else:
                    print("ERROR ADD card: ", card.errors)
        #activate card
        if 'cardAct' in request.POST:
            if Card.objects.filter(customer_ID = customer.customerID).exists():
                usedCard = Card.objects.get(customer_ID = customer.customerID, activate = True)
                new_card = Card.objects.get(card_ID=request.POST['cardAct'], customer_ID = customer.customerID)
                if usedCard.card_ID.cardID != new_card.card_ID.cardID:
                    post = request.POST.copy()
                    post['activate'] = False
                    request.POST = post
                    oldForm = activateCard(request.POST or None, instance=usedCard)
                    if oldForm.is_valid:
                        oldForm.save()
                    else:
                        print("Old card ERROR: ", oldForm.save())
                    post = request.POST.copy()
                    post['activate'] = True
                    request.POST = post
                    actForm = activateCard(request.POST or None, instance=new_card)
                    if actForm.is_valid:
                        actForm.save()
                    else:
                        print("Activate error: ", actForm.errors)
                    

    
    if Card.objects.filter(customer_ID = customer.customerID).exists():
        cardCollect = Card.objects.filter(customer_ID = customer.customerID)
        cardAll = []
        for i in range(len(cardCollect)):
            cardAll.append(cardCollect[i].card_ID)
        card = Card_details.objects.filter(card__card_ID__in=cardAll)

        mainCard = Card.objects.get(customer_ID = customer.customerID, activate = True).card_ID
        send_data = {
        'user': user,
        'customer': customer,
        'cards': card,
        'mainCard': mainCard
    }
    else:
        send_data = {
        'user': user,
        'customer': customer
    }

    
    return render(request, 'userProfile_transaction.html', send_data)




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
    # print(artist_count)
    # print(song_count)

    listen = 0
    history = ListeningHistory.objects.all()
    if history:
        for h in history:
            # print(song.artistID.artistID)
            if request.user.artist_set.filter(artistID = h.songID.artistID.artistID).exists():
                listen = listen + 1
            # print(h.songID.artistID.artistID)

    context = {'latest5Artist': latest5Artist, 'latest5Song': latest5Song,
                'artistPresent':latest5Artist[0],
                'songPresent':latest5Song[0],
                'song_count': song_count,
                'artist_count':artist_count,
                'listen': listen}

    return render(request, 'entertainmentPages/enDashboard.html', context)

def songHistoryforEntertainment(request):
    return render(request, 'entertainmentPages/songHistoryforEntertainment.html')

def enProfile (request):
    en = request.user.entertainment
    phone = en.interCode + ' ' + en.telNO if en.interCode != None and en.telNO != None else None
    context = {'phone': phone}
    return render(request, 'entertainmentPages/enProfile.html', context)

def enProfileEdit (request):
    ### show result ###
    enPresent = Entertainment.objects.get(user_id=request.user.id)
    #phone
    telNO = enPresent.interCode + enPresent.telNO if enPresent.telNO != None and enPresent.interCode != None else ''

    form = editEntertainment(instance=enPresent)
    errorflag = 0
    
    ### update ###
    if request.method == 'POST':
        if request.POST['interCode']== None or request.POST['telNO'] == None:
            messages.success(request, ('Please field your telephone number'))
            errorflag = 1

        if request.POST['interCode']== None or request.POST['telNO'] == None:
            messages.success(request, ('Please field your telephone number'))
            errorflag = 1
       

        if errorflag==0:
            form = editEntertainment(request.POST or None, request.FILES or None, instance=enPresent)
            if form.is_valid():
                form.save()
                return redirect('enProfileEdit')
        print(form.errors)

    # sending data to html
    context = {
        'telNO': telNO,
        'form': form
    }
    return render(request, 'entertainmentPages/enProfileEdit.html', context)

def showAllEntertainment (request):
    entertainments = Entertainment.objects.all().order_by('-entertainmentID')  
    list = []
    if entertainments:
        for en in entertainments:
            data = {
                'entertainmentID': en.entertainmentID,
                'entertainmentName': en.entertainmentName,
                'phone': en.interCode + ' ' + en.telNO if en.interCode != None and en.telNO != None else None
            }
            list.append(data)

        context = {'entertainments': list}
    else:
        context = {}

    return render(request, 'entertainmentPages/ADallEntertainmentTable.html', context)

def singleEntertainment (request, pk):
    en = Entertainment.objects.get(entertainmentID = pk)
    phone = en.interCode + ' ' + en.telNO if en.interCode != None and en.telNO != None else None
    artists = Artist.objects.filter(entertainmentID = en.user_id)

    thisEnArtistID = []
    if artists:
        for a in artists:
            thisEnArtistID.append(a.artistID)

    listen = 0
    history = ListeningHistory.objects.all()
    if history:
        for h in history:
            if h.songID.artistID.artistID in thisEnArtistID:
                listen = listen + 1
                
    context = {
        'en': en,
        'phone': phone,
        'artists': artists,
        'listen': listen
    }
    return render(request, 'entertainmentPages/ADsingleEntertainment.html', context)

def deleteEntertianment (request, pk):
    en = Entertainment.objects.get(entertainmentID = pk)
    user = User.objects.get(id = en.user_id)
    c_artist = Artist.objects.filter(entertainmentID = en.user_id)
    
    print(user.username)
    song_count = 0
    allSong = Song.objects.all()
    for song in allSong:
        # print(song.artistID.artistID)
        if user.artist_set.filter(artistID = song.artistID.artistID).exists():
            song_count = song_count + 1

        
    if request.method == 'POST':
       user.delete()
       return redirect('adminDashboard')

    context = {'en': en, 'song_count':  song_count, 'artist_count': len(c_artist)}

    return render(request, 'entertainmentPages/ADdeleteEntertainment.html', context)

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
            return redirect('adminDashboard')
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

def adminDashboard(request):
    c_song = Song.objects.count()
    c_artist = Artist.objects.count()
    c_en = Entertainment.objects.count()
    c_customer = Customer.objects.count()

    index = 0

    latest5Song = [None, None, None, None, None]
    allSong = Song.objects.all().order_by('-songID')
    for song in allSong:
        # print(song.artistID.artistID)
        if index < 5:
            latest5Song[index] = song
            index = index + 1
    
    index = 0
    latest5Customer = [None, None, None, None, None]
    allCust = Customer.objects.all().order_by('-customerID')
    for customer in allCust:
        # print(song.artistID.artistID)
        if index < 5:
            latest5Customer[index] = customer
            index = index + 1

    context = {
        'c_song': c_song,
        'c_artist': c_artist,
        'c_en': c_en,
        'c_customer': c_customer,
        'latest5Song': latest5Song,
        'latest5Customer': latest5Customer,
    }

    return render(request, 'adminPages/adDashboard.html', context)

#  ------------------------------ Artist ------------------------------------
def ADaddArtist(request):
    form = addArtistForm()
    if request.method == 'POST':
        errorFlag = 0

        form = addArtistForm(request.POST or None, request.FILES or None)

        artistName = request.POST.get('artistName')
        entertainmentID = request.POST.get('entertainmentID')
        dob = request.POST.get('dob')

        if not (Entertainment.objects.filter(entertainmentID = entertainmentID).exists()):
            messages.success(request, ('entertainment ID not found'))
            errorFlag = 1

        context = {'artistName':artistName, 'dob':dob, 'entertainmentID': entertainmentID}
     
        #Is form valid?
        if errorFlag == 0:
            if form.is_valid():
                en = Entertainment.objects.get(entertainmentID = entertainmentID)
                print(en.user_id)
                # ----------- Add FK autometically -----------
                addArtistFK = form.save(commit=False)
                addArtistFK.entertainmentID = User.objects.get(id = en.user_id)
                addArtistFK.save()
                print('success')
                if request.user.groups.all()[0].name == 'entertainment':
                    return redirect('enDashboard')
                if request.user.groups.all()[0].name == 'admin':
                    return redirect('adminDashboard')
        print(form.errors)
        print('not success')
        return render(request, 'artistPages/ADaddArtist.html', context)

    else:
        return render(request, 'artistPages/ADaddArtist.html')

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
                return redirect('adminDashboard')
        else:
            print(form.errors)
            print('not success')
            return render(request, 'artistPages/addArtist.html', context)

    else:
        return render(request, 'artistPages/addArtist.html')

def showAllArtist (request):
    if request.user.groups.all()[0].name == 'entertainment':
        context = {'artists': request.user.artist_set.all().order_by('-artistID')}
        return render(request, 'artistPages/allArtistTable.html', context)

    if request.user.groups.all()[0].name == 'admin':
        context = {'artists': Artist.objects.all().order_by('-artistID')}
        print(context)
        return render(request, 'artistPages/ADallArtistTable.html', context)

    return redirect('landingPage')

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
                return redirect('adminDashboard')
        else:
            print(form.errors)
            print('not success')
            if request.user.groups.all()[0].name == 'entertainment':
                return render(request, 'artistPages/updateArtist.html',{'form': form, 'artist': artist})
            if request.user.groups.all()[0].name == 'admin':
                return render(request, 'artistPages/ADupdateArtist.html', {'form': form, 'artist': artist})
    else:        
        if request.user.groups.all()[0].name == 'entertainment':
            return render(request, 'artistPages/updateArtist.html',{'form': form, 'artist': artist})
        if request.user.groups.all()[0].name == 'admin':
            return render(request, 'artistPages/ADupdateArtist.html', {'form': form, 'artist': artist})

def deleteArtist (request, pk):
    artist = Artist.objects.get(artistID = pk)
    en = User.objects.get(id = artist.entertainmentID_id)
    en = en.entertainment
    artist_song = artist.song_set.count()
    if request.method == 'POST':
        artist.delete()
        if request.user.groups.all()[0].name == 'entertainment':
            return redirect('enDashboard')
        if request.user.groups.all()[0].name == 'admin':
            return redirect('adminDashboard')

    context = {'artist': artist, 'count': artist_song, 'en': en}
    if request.user.groups.all()[0].name == 'entertainment':
        return render(request, 'artistPages/deleteArtist.html', context)
    if request.user.groups.all()[0].name == 'admin':
        return render(request, 'artistPages/ADdeleteArtist.html', context)

def singleArtist(request, pk):
    artist = Artist.objects.get(artistID = pk)
    en = User.objects.get(id = artist.entertainmentID_id)
    en = en.entertainment
    artist_song = artist.song_set.all()
    count = artist.song_set.count()
    context = {'artist': artist, 'count': count, 'artist_song': artist_song, 'en': en}

    if request.user.groups.all()[0].name == 'entertainment':
        return render(request, 'artistPages/singleArtist.html', context)
    if request.user.groups.all()[0].name == 'admin':
        return render(request, 'artistPages/ADsingleArtist.html', context)


#  ------------------------------ Song ------------------------------------

def showAllSong(request):
    songs = []

    allSong = Song.objects.all().order_by('-songID')
    if request.user.groups.all()[0].name == 'entertainment':
        for song in allSong:
            # print(song.artistID.artistID)
            if request.user.artist_set.filter(artistID = song.artistID.artistID).exists():
                songs.append(song)
        context = {'songs': songs}

        return render(request, 'songPages/allSongTable.html', context)

    if request.user.groups.all()[0].name == 'admin':
        context = {'songs': allSong}
        return render(request, 'songPages/ADallSongTable.html', context)

    return redirect('landingPage')


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
                    return redirect('adminDashboard')
        print(form.errors)
        print('not success')
        if request.user.groups.all()[0].name == 'entertainment':
            return render(request, 'songPages/updateSong.html', {'form': form, 'song': song})
        if request.user.groups.all()[0].name == 'admin':
            return render(request, 'songPages/ADupdateSong.html', {'form': form, 'song': song})
    else:
        # return render(request, 'updateSong.html', {'song': song})
        if request.user.groups.all()[0].name == 'entertainment':
            return render(request, 'songPages/updateSong.html', {'form': form, 'song': song})
        if request.user.groups.all()[0].name == 'admin':
            return render(request, 'songPages/ADupdateSong.html', {'form': form, 'song': song})

def deleteSong (request, pk):
    song = Song.objects.get(songID = pk)
    if request.method == 'POST':
        song.delete()
        if request.user.groups.all()[0].name == 'entertainment':
            return redirect('enDashboard')
        if request.user.groups.all()[0].name == 'admin':
            return redirect('adminDashboard')

    context = {'song': song}
    if request.user.groups.all()[0].name == 'entertainment':
        return render(request, 'songPages/deleteSong.html', context)
    if request.user.groups.all()[0].name == 'admin':
        return render(request, 'songPages/ADdeleteSong.html', context)

    return redirect('langingPage')

def singleSong (request, pk):
    song = Song.objects.get(songID = pk)
 
    listen = 0
    history = ListeningHistory.objects.all()
    if history:
        for h in history:
            print(song.artistID.artistID)
            # if request.user.artist_set.filter(artistID = h.songID.artistID.artistID).exists():
            if h.songID.songID == song.songID:
                listen = listen + 1

    context = {'song': song, 'listen': listen}
    if request.user.groups.all()[0].name == 'entertainment':
        return render(request, 'songPages/singleSong.html', context)
    if request.user.groups.all()[0].name == 'admin':
        return render(request, 'songPages/ADSingleSong.html', context)

    return redirect('langingPage')

def showAllcustomer (request):
    customers = Customer.objects.all().order_by('-customerID')
    context = {'customers': customers}
    return render(request, 'adminPages/ADallCustomerTable.html', context)



def deleteCustomer (request, pk):
    customer = Customer.objects.get(customerID = pk)
    user = User.objects.get(id = customer.user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('adminDashboard')

    customerUsername = user.username

    context = {'customerUsername': customerUsername, 'customer': customer}
    return render (request, 'adminPages/ADdeleteCustomer.html', context)


def singleCustomer (request, pk):
    customer = Customer.objects.get(customerID = pk)
    user = User.objects.get(id = customer.user_id)
    customerUsername = user.username
    phone = customer.interCode + ' ' + customer.telNO if customer.interCode != None and customer.telNO != None else None
  
    age = None
    if customer.dob != None:
        birth = customer.dob
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    context = {'customerUsername': customerUsername, 'customer': customer, 'phone': phone, 'age': age}
    return render (request, 'adminPages/ADsingleCustomer.html', context)