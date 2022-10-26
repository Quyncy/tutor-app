from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from user.models import *

class DozentForm(forms.Form):
    class Meta:
        model = Dozent
        fields = '__all__'
        labels = {
            'title': _('Enter title'),
            'name': _('Enter first_name'),
            'last_name': _('Enter last name'),
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