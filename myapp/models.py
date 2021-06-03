from django.db import models
# from django.db.models.deletion import CASCADE

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
    
    def genID():
        n = Entertainment.objects.count()
        return "EN" + str(n).zfill(6)

    # entertainmentID = models.AutoField(primary_key=True)
    entertainmentID = models.CharField(max_length=8, default=genID ,primary_key=True)
    entertainmentName = models.CharField(max_length=30) 
    enUserName = models.CharField(max_length=12)
    password = models.CharField(max_length=12)
    interCode = models.CharField(max_length=4)
    telNO = models.CharField(max_length=20) 
    address = models.TextField()
    email = models.CharField(max_length=30)


#Admin Table
# class Admin (models.Model):

#     def genID():
#         n = Entertainment.objects.count()
#         return "AD" + str(n).zfill(6)

#     # entertainmentID = models.AutoField(primary_key=True)
#     adminID = models.CharField(max_length=8, default=genID ,primary_key=True)
#     adminName = models.CharField(max_length=12) 
#     enUserName = models.CharField(max_length=12)
#     password = models.CharField(max_length=12)
#     interCode = models.CharField(max_length=4)
#     telNO = models.CharField(max_length=20) 
#     address = models.TextField()
#     email = models.CharField(max_length=30)