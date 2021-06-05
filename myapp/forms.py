from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

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
class addArtist (ModelForm):
    class Meta:
        model = Artist
        fields = ['artistName', 'profileImage', 'dob']

# Edit Customer infomation
class editCusInfo (ModelForm):
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'gender', 'profileImage', 'dob'] #'interCode', 'telNO'