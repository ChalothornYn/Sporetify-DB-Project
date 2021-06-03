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
    path('history/', views.AdminHistory),
    path('userprofile/', views.userProfile),
    path('adminprofile/', views.adminProfile),
    path('song/', views.songHome),
    path('songtest/', views.songTest),
    path('song/edm/', views.songEDM),
    path('userprofile/edit/', views.userProfile_edit),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
