from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.enter, name='account'),
    path('main', views.viewing, name='main'),
    path('contacts', views.contacts, name='contacts'),
    path('about', views.about, name='about'),
    path('main/create', views.create, name='account_create'),
    path('main/home', views.home, name='home'),
    path('main/new', views.new, name='new'),
    # path('upload/', views.upload_image, name = 'upload_image'),
]
