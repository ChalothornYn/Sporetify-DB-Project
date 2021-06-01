from django.db import models
# from django.db.models.deletion import CASCADE

# Create your models here.  # NOT NULL is DEFAULT

# Song Table
class Song (models.Model):  
    songID = models.AutoField(primary_key=True)
    songName = models.CharField(max_length=20)
    artistID = models.ForeignKey('Artist', on_delete=models.CASCADE)
    songImg = models.ImageField(upload_to='uploads/songImg/')
    normalURL = models.FileField(upload_to='uploads/songQuality/normal/')
    goodURL = models.FileField(upload_to='uploads/songQuality/good/')
    genre1 = models.CharField(max_length=20)
    genre2 = models.CharField(max_length=20, null=True)
    genre3 = models.CharField(max_length=20, null=True)
    album = models.CharField(max_length=30, null=True)
    lyrics = models.TextField()
    description = models.TextField()
    language = models.CharField(max_length=2)

#Artist Table
class Artist (models.Model):
    artistID = models.AutoField(primary_key=True)
    artiseName = models.CharField(max_length=20)
    dob = models.DateField()
    entertainmentID = models.ForeignKey('Entertainment', on_delete=models.CASCADE)

#Entertainment Table
class Entertainment (models.Model):
    entertainmentID = models.AutoField(primary_key=True)
    entertainmentName = models.CharField(max_length=30)
    enUserName = models.CharField(max_length=12)
    password = models.CharField(max_length=12)
    interCode = models.CharField(max_length=4)
    telNO = models.CharField(max_length=20) 
    address = models.TextField()
    email = models.CharField(max_length=30)

