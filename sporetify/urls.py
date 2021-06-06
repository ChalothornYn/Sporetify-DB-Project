"""sporetify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from collections import namedtuple
from django.contrib import admin
from django.urls import path
from myapp import views

# For upload img
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landingPage, name='landingPage'),

    path('addsong/', views.addSong, name='addSong'),
    path('song/all/', views.showAllSong, name='showAllSong'),
    path('song/single/<str:pk>/', views.singleSong, name='singleSong'),
    path('update/song/<str:pk>/', views.updateSong, name='updateSong'),
    path('delete/song/<str:pk>/', views.deleteSong, name='deleteSong'),

    path('addartist/', views.addArtist, name='addArtist'),
    path('artist/all/', views.showAllArtist, name='showAllArtist'),
    path('artist/single/<str:pk>/', views.singleArtist, name='singleArtist'),
    path('update/artist/<str:pk>/', views.updateArtist, name='updateArtist'),
    path('delete/artist/<str:pk>/', views.deleteArtist, name='deleteArtist'),


    # path('addsongsubmit/', views.addSongSubmit),
    path('testtable/', views.Testtable),

    #SONG URL
    path('song/', views.viewSong),
    path('songtest/', views.songTest),
    path('songtestjs/', views.Songtestjs),
    path('song/edm/', views.songEDM),
    path('song/playsong/', views.playSong),

  

    #User URL
    path('login/', views.loginUser, name='login'),
    path('signup/', views.signupUser, name='signup'),
    path('userprofile/', views.userProfile),
    path('userprofile/edit/', views.userProfile_edit),
    path('userprofile/package', views.userProfile_package),
    path('userprofile/transaction', views.userProfile_transaction),
    path('userprofile/family', views.userProfile_family),

    # Entertainment URL
    path('signup/entertainment/', views.signupEntertainment, name='enSignup'),
    path('login/entertainment/', views.loginEntertainment, name='enLogin'),
    path('en/dashboard', views.enDashboard, name='enDashboard'),
    path('en/Profile', views.enProfile, name='enProfile'),

    # Admin URL
    path('adminregister/', views.adminRegister, name='adminRegister'),
    path('adminlogin/', views.adminLogin, name='adminLogin'),
    path('adminlogout/', views.adminLogout, name='adminLogout'),
    path('adminprofile/', views.adminProfile, name='adminProfile'),
    path('history/', views.AdminHistory),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
