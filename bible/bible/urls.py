"""bible URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from invertedIndex import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('ASV/', views.indexASV),
    path('KJV/', views.indexKJV),
    path('MKJV/', views.indexMKJV),
    path('NHEB/', views.indexNHEB),
    path('RSV/', views.indexRSV),
    path('ASV/result/', views.preprocessingInputASV),
    path('KJV/result/', views.preprocessingInputKJV),
    path('MKJV/result/', views.preprocessingInputMKJV),
    path('NHEB/result/', views.preprocessingInputNHEB),
    path('RSV/result/', views.preprocessingInputRSV),
]
