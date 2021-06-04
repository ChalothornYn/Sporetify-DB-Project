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
    path('', views.landingPage),
    path('login/', views.Login),
    path('signup/', views.Signup),
    path('signupen/', views.SignupEn),
    path('home/', views.home),
    path('addsong/', views.addSong),
    path('addsongsubmit/', views.addSongSubmit),
    path('testtable/', views.Testtable),
    path('song/', views.songHome),
    path('songtest/', views.songTest),
    path('song/edm/', views.songEDM),

    #User URL
    path('userprofile/', views.userProfile),
    path('userprofile/edit/', views.userProfile_edit),
    path('userprofile/package', views.userProfile_package),
    path('userprofile/transaction', views.userProfile_transaction),

    # Entertainment URL
    path('en/profile', views.enProfile, name='enProfile'),
    


    # Admin URL
    path('adminregister/', views.adminRegister, name='adminRegister'),
    path('adminlogin/', views.adminLogin, name='adminLogin'),
    path('adminlogout/', views.adminLogout, name='adminLogout'),
    path('adminprofile/', views.adminProfile, name='adminProfile'),
    path('history/', views.AdminHistory),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
