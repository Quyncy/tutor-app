from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # TESTE dozent, usw. FORM
    path('dozent/', views.dozent, name='dozent'),
    path('module/', views.module, name='module'),
    path('tutor/', views.tutor, name='tutor'),
    path('tutorprofile/', views.tutorprofile, name='tutorprofile'),
    path('kursleiter/', views.kursleiter, name='kursleiter'),
    path('kursleiterprofile/', views.kursleiterprofile, name='kursleiterprofile'),
    path('user/', views.user, name='user'),


    # Ok - Erfolgreich gespeichert
    path('ok/', views.ok, name='ok'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]