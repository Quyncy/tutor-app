from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # TESTE dozent, usw. FORM
    path('dozent/', views.dozent, name='dozent'),
    path('module/', views.module, name='module'),
    path('student/', views.student, name='student'),
    path('teacher/', views.student, name='student'),
    path('user/', views.student, name='student'),


    # Ok - Erfolgreich gespeichert
    path('ok/', views.ok, name='ok'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]