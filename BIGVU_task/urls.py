from django.urls import path

# from django.conf import u
from django.urls import path, include
from django.views.generic import ListView, DetailView


from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('course/<str:question_id>', views.course, name='course'),

]