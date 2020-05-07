"""myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('statistics', views.statistics),
    path('plot', views.plot),
    path('charts', views.charts),
    path('aboutUs', views.aboutUs),
    path('login', views.login),
    path('handleLogin', views.handleLogin),
    path('handleLoginOut', views.handleLoginOut),
    path('page_ajax', views.page_ajax),
    path('detail', views.detail),
    path('searchResult', views.searchResult),
    path('calculation', views.calculation),
    path('calculation_mode2', views.calculation_mode2),
    path('calculation_mode3', views.calculation_mode3),
    path('plot_normal', views.plot_normal),
]
