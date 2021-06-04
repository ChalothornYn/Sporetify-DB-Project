from django.db.models import fields
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Add new song 
class addSongForm (ModelForm):
    class Meta:
        model = Song
        fields = ['songName', 'artistID', 'songImg', 'normalURL', 'goodURL', 'genre1', 'genre2', 'genre3', 'album', 'lyrics', 'description', 'language'] 

# Add new admin
class addAdmin (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']