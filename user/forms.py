from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from user.models import *

from django.contrib import admin

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['username','date_joined','last_login',]

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model=StudentProfile
        fields='__all__'

        label = {
            'user': _('Vorname'),
            'student_id': _('ID'),
            'kurs': _('Kurs'),
            'work_hours': _('Arbeitsstunden'),
            'anzahl_korrekturen': _('Anzahl Korrekturen'),
        }
        error_messages = {
            'user':{
                'required': ('Vorname angeben')
            }
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['username','date_joined','last_login',]

class UserForm(forms.ModelForm):
    """ Bei Admin eingaben werden die fields ignoriert """
    class Meta:
        model = User
        exclude = ['username','date_joined','last_login',]

# class PersonAdmin(admin.ModelAdmin):
#     form = StudentForm

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = '__all__'
        label = {
            'user': _('User'),
            'teacher_id': _('Teacher ID'),
        }


class DozentForm(forms.ModelForm):
    class Meta:
        model = Dozent
        fields = '__all__'
        labels = {
            'title': _('Titel eingeben'),
            'name': _('Vorname eingeben'),
            'nachname': _('Nachname eingeben'),
        }
        error_messages = {
            'title':{
                'required': _('Title has to be choosen')
            },
            'name':{
                'required': _('First name has to be entered')
            },
            'nachname': _('Last name has to be entered')
        },


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'
        # exclude=

        # labels := Bezeichnung
        labels = {
            'module_name': _('Kursname eingeben'),
            'description': _('Beschreibung eingegeben'),
            'dozent': _('Dozent eingeben'),
            'teacher': _('Kursleiter eingeben'),
            'semester': _('Semester eingegeben'),
        }
        error_messages = {
            fields : {
                'module_name': {
                    'required': _('Module name has to be entered')
                },
                'description': {
                    'required': _('Description has to be entered')
                },
                'dozent': {
                    'required': _('Dozent has to be entered')
                },
                'Teacher': {
                    'required': _('Teacher has to be entered')
                },
                'semester': {
                    'required': _('Semester has to be entered')
                },
            }
        }
