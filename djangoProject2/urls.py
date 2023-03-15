from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('BIGVU_task.urls')),

]