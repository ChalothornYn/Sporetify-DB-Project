from django.db.models import fields
from django.forms import ModelForm
from .models import Song

class addSongForm (ModelForm):
    class Meta:
        model = Song
        fields = ['songName', 'artistID', 'songImg', 'normalURL', 'goodURL', 'genre1', 'genre2', 'genre3', 'album', 'lyrics', 'description', 'language'] 

        # still got error songImg normalURL goodURL hot found value