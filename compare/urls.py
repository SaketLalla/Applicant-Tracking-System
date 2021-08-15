from django.contrib import admin
from django.urls import path , include
from compare import views
urlpatterns = [
    path('', views.compare)

]