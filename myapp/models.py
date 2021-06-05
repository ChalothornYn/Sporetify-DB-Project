from django.db import models
from django.contrib.auth.models import User

# Create your models here.  # NOT NULL is DEFAULT


# Song Table
class Song (models.Model):  

    def genID():
        n = Song.objects.count()
        return "S" + str(n).zfill(9)

    # songID = models.AutoField(primary_key=True)
    songID = models.CharField(max_length=10, default=genID ,primary_key=True)
    songName = models.CharField(max_length=100)
    artistID = models.ForeignKey('Artist', on_delete=models.CASCADE)
    songImg = models.ImageField(upload_to='uploads/songImg/')
    normalURL = models.FileField(upload_to='uploads/songQuality/normal/')
    goodURL = models.FileField(upload_to='uploads/songQuality/good/')
    genre1 = models.CharField(max_length=20)
    genre2 = models.CharField(max_length=20, null=True)
    genre3 = models.CharField(max_length=20, null=True)
    album = models.CharField(max_length=100, null=True)
    lyrics = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=2)


#Artist Table
class Artist (models.Model):

    def genID():
        n = Artist.objects.count()
        return "AT" + str(n).zfill(6)
    
    # artistID = models.AutoField(primary_key=True)
    artistID = models.CharField(max_length=8, default=genID ,primary_key=True)
    artistName = models.CharField(max_length=50)
    dob = models.DateField()
    entertainmentID = models.ForeignKey('Entertainment', on_delete=models.CASCADE)


#Entertainment Table
class Entertainment (models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    entertainmentName = models.CharField(max_length=30, default='No data', blank=False) 
    profileImage = models.ImageField(upload_to='uploads/profileImage/admin/', default = 'uploads/profileImage/profile-placeholder.png')
    interCode = models.CharField(max_length=4, null=True)
    telNO = models.CharField(max_length=20, null=True, unique=True) 
    address = models.TextField(null=True)


# Admin Table
class Admin (models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=50, default='No data', blank=False)
    lastName = models.CharField(max_length=50, default='No data', blank=False)
    gender = models.CharField(max_length=1, choices=[('M','MALE'), ('F','FEMALE'), ('O', 'OTHER')], null=True)
    profileImage = models.ImageField(upload_to='uploads/profileImage/admin/', default = 'uploads/profileImage/profile-placeholder.png')
    interCode = models.CharField(max_length=4, null=True)
    telNO = models.CharField(max_length=20, null=True, unique=True) 
    dob = models.DateField(null=True)

# User Table
class Customer (models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=50, default='No data', blank=False)
    lastName = models.CharField(max_length=50, default='No data', blank=False)
    gender = models.CharField(max_length=1, choices=[('M','MALE'), ('F','FEMALE'), ('O', 'OTHER')], null=True)
    profileImage = models.ImageField(upload_to='uploads/profileImage/user/', default = 'uploads/profileImage/profile-placeholder.png')
    interCode = models.CharField(max_length=4, null=True)
    telNO = models.CharField(max_length=20, null=True, unique=True) 
    dob = models.DateField(null=True)
    packageID = models.ForeignKey('Package', on_delete=models.CASCADE)

# Package Table
class Package (models.Model):
    packageID = models.CharField(max_length=4, primary_key=True)
    packageName = models.CharField(max_length=30)
    packagePrice = models.DecimalField(max_digits=8, decimal_places=2)
    packageDuration = models.DurationField()