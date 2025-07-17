"""ElevateXIndia URL Configuration

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
from django.urls import path,include
from Main import views



urlpatterns = [
    path('', views.home, name='Home Page'),
    path('index/', views.home, name='Home Page'),
    path('home/', views.home, name='Home Page'),
    path('services/', views.services, name='our Services'),
    path('about/', views.about, name='About Us Page'),
    path('aboutus/', views.about, name='About Us Page'),
    path('contact/', views.contact, name='Contact Us Page'),
    path('contactus/', views.contact, name='Contact Us Page'),
    path('signin/', views.signin, name='Sign-In page'),
    path('login/', views.signin, name='Sign-In page'),
    path('signup/', views.signup, name='Sign-Up Page'),
    path('recovery/', views.recovery, name='Password-Recovery page'),
    path('reset/', views.recovery, name='Password-Recovery page'),
    path('maintenance/', views.maintenance, name='Maintenance Page'),
    path('comingsoon/', views.comingsoon, name='Coming Soon'),
    path('coming/', views.comingsoon, name='Comming Soon'),
    path('404/', views.Page404, name='404 Page'),
    path('error404/', views.Page404, name='404 Page'),
    path('pagenotfound/', views.Page404, name='404 Page'),
    path('welcome/', views.welcome, name='welcome'),
    path('success/', views.success, name='Success'),
    path('denied/', views.denied, name='Denied'),
    path('blocked/', views.denied, name='denied'),
    path('qr/lakhiramdairyfarm/menu', views.redirect_to_lakhiram, name='redirect-to-lakhiram'),
    path('qr/lakhiramdairyfarm/lassi', views.redirect_to_lakhiram, name='redirect-to-lakhiram'),
    path('qr/lakhiramdairyfarm/milk', views.redirect_to_lakhiram, name='redirect-to-lakhiram'),
    path('Project/tracking/id/id_of_project', views.tracking, name='Tracking Page'),

]
