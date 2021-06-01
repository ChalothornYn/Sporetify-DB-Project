from django.db.models import fields
from django.forms import ModelForm
from .models import Song

class addSongForm (ModelForm):
    class Meta:
        model = Song
        fields = ['songName', 'artistID', 'songImg', 'normalURL', 'goodURL', 'genre1', 'genre2', 'genre3', 'album', 'lyrics', 'description', 'language'] 

        # still got error songImg normalURL goodURL hot found value

    # songID = models.AutoField(primary_key=True)
    # songName = models.CharField(max_length=20)
    # artistID = models.ForeignKey('Artist', on_delete=models.CASCADE)
    # songImg = models.ImageField(upload_to='uploads/songImg/')
    # normalURL = models.FileField(upload_to='uploads/songQuality/normal/')
    # goodURL = models.FileField(upload_to='uploads/songQuality/good/')
    # genre1 = models.CharField(max_length=20)
    # genre2 = models.CharField(max_length=20, null=True)
    # genre3 = models.CharField(max_length=20, null=True)
    # album = models.CharField(max_length=30, null=True)
    # lyrics = models.TextField()
    # description = models.TextField()
    # language = models.CharField(max_length=