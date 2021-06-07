from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Add new song 
class addSongForm (ModelForm):
    class Meta:
        model = Song
        fields = ['songName', 'artistID', 'songImg', 'normalURL', 'goodURL', 'genre1', 'genre2', 'genre3', 'album', 'lyrics', 'description', 'language'] 

# Add Entertainment User
class addEntertainment (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Add new admin
class addAdmin (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Add new customer
class addCustomer (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Add new artist
class addArtistForm (ModelForm):
    class Meta:
        model = Artist
        fields = ['artistName', 'profileImage', 'dob']

# Edit Customer infomation
class editCusInfo (ModelForm):
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'gender', 'profileImage', 'dob', 'interCode', 'telNO'] #

# Edit Customer infomation
class editCusInfo (ModelForm):
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'gender', 'profileImage', 'dob', 'interCode', 'telNO'] #

# Change customer package
class packCusInfo (ModelForm):
    class Meta:
        model = Customer
        fields = ['packageID']

class editEntertainment (ModelForm):
    class Meta:
        model = Entertainment
        fields = ['entertainmentName', 'profileImage', 'interCode', 'telNO', 'address'] 
        
# Add family
class addFamily (ModelForm):
    class Meta:
        model = Family
        fields = ['manager']

# changeFamily
class changeFamily (ModelForm):
    class Meta:
        model = Customer
        fields = ['familyID']

class manageFamily (ModelForm):
    class Meta:
        model = Customer
        fields = ['familyID', 'packageID']

# card_details
class addCard (ModelForm):
    class Meta:
        model = Card_details
        fields = ['cardID', 'cardType', 'expireDate', 'cvv']

class collectCard(ModelForm):
    class Meta:
        model = Card
        fields = ['customer_ID', 'card_ID', 'activate']