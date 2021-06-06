from django.db import models
from django.contrib.auth.models import User

# Create your models here.  # NOT NULL is DEFAULT


# Song Table
class Song (models.Model):  

    def genID():
        n = Song.objects.count()
        return "S" + str(n).zfill(9)

    MAIN_GENRE_CHOICES = [
        ('EDM', 'EDM'),
        ('Rap', 'Rap'),
        ('Rock', 'Rock'),
        ('Pop', 'Pop'),
        ('R&B', 'R&B'),
        ('Latin', 'Latin'),
    ]

    GENRE_CHOICES = [
        ('none', 'none'),
        ('EDM', 'EDM'),
        ('Rap', 'Rap'),
        ('Rock', 'Rock'),
        ('Pop', 'Pop'),
        ('R&B', 'R&B'),
        ('Latin', 'Latin'),
    ]

    LANGUAGE_CHOICES = [
        ('af', 'Afrikaans'),
        ('SQ','Albanian'),
        ('AR','Arabic'),
        ('HY','Armenian'),
        ('EU','Basque'),
        ('BN','Bengali'),
        ('BG','Bulgarian'),
        ('CA','Catalan'),
        ('KM','Cambodian'),
        ('ZH','Chinese (Mandarin)'),
        ('HR','Croatian'),
        ('CS','Czech'),
        ('DA','Danish'),
        ('NL','Dutch'),
        ('EN','English'),
        ('ET','Estonian'),
        ('FJ','Fiji'),
        ('FI','Finnish'),
        ('FR','French'),
        ('KA','Georgian'),
        ('DE','German'),
        ('EL','Greek'),
        ('GU','Gujarati'),
        ('HE','Hebrew'),
        ('HI','Hindi'),
        ('HU','Hungarian'),
        ('IS','Icelandic'),
        ('ID','Indonesian'),
        ('GA','Irish'),
        ('IT','Italian'),
        ('JA','Japanese'),
        ('JW','Javanese'),
        ('KO','Korean'),
        ('LA','Latin'),
        ('LV','Latvian'),
        ('LT','Lithuanian'),
        ('MK','Macedonian'),
        ('MS','Malay'),
        ('ML','Malayalam'),
        ('MT','Maltese'),
        ('MI','Maori'),
        ('MR','Marathi'),
        ('MN','Mongolian'),
        ('NE','Nepali'),
        ('NO','Norwegian'),
        ('FA','Persian'),
        ('PL','Polish'),
        ('PT','Portuguese'),
        ('PA','Punjabi'),
        ('QU','Quechua'),
        ('RO','Romanian'),
        ('RU','Russian'),
        ('SM','Samoan'),
        ('SR','Serbian'),
        ('SK','Slovak'),
        ('SL','Slovenian'),
        ('ES','Spanish'),
        ('SW','Swahili'),
        ('SV','Swedish'),
        ('TA','Tamil'),
        ('TT','Tatar'),
        ('TE','Telugu'),
        ('TH','Thai'),
        ('BO','Tibetan'),
        ('TO','Tonga'),
        ('TR','Turkish'),
        ('UK','Ukrainian'),
        ('UR','Urdu'),
        ('UZ','Uzbek'),
        ('VI','Vietnamese'),
        ('CY','Welsh'),
        ('XH','Xhosa'),
    ]

    songID = models.CharField(max_length=10, default=genID ,primary_key=True)
    songName = models.CharField(max_length=100)
    artistID = models.ForeignKey('Artist', on_delete=models.CASCADE)
    songImg = models.ImageField(upload_to='uploads/songImg/')
    normalURL = models.FileField(upload_to='uploads/songQuality/normal/')
    goodURL = models.FileField(upload_to='uploads/songQuality/good/')
    genre1 = models.CharField(max_length=20, choices=MAIN_GENRE_CHOICES, default='none')
    genre2 = models.CharField(max_length=20, choices=GENRE_CHOICES, default='none')
    genre3 = models.CharField(max_length=20, choices=GENRE_CHOICES, default='none')
    album = models.CharField(max_length=100, null=True, blank=True, default='')
    lyrics = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)


#Artist Table
class Artist (models.Model):

    def __str__(self):
        return self.artistName + " | " + self.artistID

    def genID():
        n = Artist.objects.count()
        return "AT" + str(n).zfill(6)
    
    artistID = models.CharField(max_length=8, default=genID ,primary_key=True)
    artistName = models.CharField(max_length=50)
    profileImage = models.ImageField(upload_to='uploads/profileImage/artist/', default = 'uploads/profileImage/profile-placeholder.png')
    dob = models.DateField()
    entertainmentID = models.ForeignKey(User, on_delete=models.CASCADE)


#Entertainment Table
class Entertainment (models.Model):
    def genID():
        n = Entertainment.objects.count()
        return "EN" + str(n).zfill(6)

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    entertainmentID = models.CharField(max_length=8, default=genID)
    entertainmentName = models.CharField(max_length=30, default='No data', blank=False) 
    profileImage = models.ImageField(upload_to='uploads/profileImage/entertainment/', default = 'uploads/profileImage/profile-placeholder.png')
    interCode = models.CharField(max_length=4, null=True)
    telNO = models.CharField(max_length=20, null=True, unique=True) 
    address = models.TextField(null=True)

# Admin Table
class Admin (models.Model):
    def genID():
        n = Admin.objects.count()
        return "AD" + str(n).zfill(6)

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    adminID =  models.CharField(max_length=8, default=genID)
    firstName = models.CharField(max_length=50, default='No data', blank=False)
    lastName = models.CharField(max_length=50, default='No data', blank=False)
    gender = models.CharField(max_length=1, choices=[('M','MALE'), ('F','FEMALE'), ('O', 'OTHER')], null=True)
    profileImage = models.ImageField(upload_to='uploads/profileImage/admin/', default = 'uploads/profileImage/profile-placeholder.png')
    interCode = models.CharField(max_length=4, null=True)
    telNO = models.CharField(max_length=20, null=True, unique=True) 
    dob = models.DateField(null=True)

# Customer Table
class Customer (models.Model):
    DEFAULT_PACKKAGE = "PF00"
    def genID():
        n = Customer.objects.count()
        return "U" + str(n).zfill(7)

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    customerID =  models.CharField(max_length=8, default=genID)
    firstName = models.CharField(max_length=50, default='No data', blank=False)
    lastName = models.CharField(max_length=50, default='No data', blank=False)
    gender = models.CharField(max_length=1, choices=[('M','MALE'), ('F','FEMALE'), ('O', 'OTHER')], null=True)
    profileImage = models.ImageField(upload_to='uploads/profileImage/user/', default = 'uploads/profileImage/profile-placeholder.png')
    interCode = models.CharField(max_length=4, null=True)
    telNO = models.CharField(max_length=20, null=True, unique=True) 
    dob = models.DateField(null=True)
    packageID = models.ForeignKey('Package', on_delete=models.CASCADE, default=DEFAULT_PACKKAGE)
    familyID = models.ForeignKey('Family', on_delete=models.CASCADE, null=True)

# Family Table
class Family (models.Model):
    def genID():
        n = Family.objects.count()
        return "F" + str(n).zfill(7)
    familyID = models.CharField(max_length=8, default=genID ,primary_key=True)
    manager = models.CharField(max_length=8)

# Package Table
class Package (models.Model):
    packageID = models.CharField(max_length=4, primary_key=True)
    packageName = models.CharField(max_length=30)
    packagePrice = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    packageDuration = models.DurationField(null=True)