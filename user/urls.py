from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # TESTE dozent, usw. FORM
    path('dozent/', views.dozent, name='dozent'),
    path('module/', views.module, name='module'),
    path('student/', views.student, name='student'),
    path('studentprofile/', views.studentprofile, name='studentprofile'),
    path('teacher/', views.teacher, name='teacher'),
    path('teacherprofile/', views.teacherprofile, name='teacherprofile'),
    path('user/', views.user, name='user'),


    # Ok - Erfolgreich gespeichert
    path('ok/', views.ok, name='ok'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]