from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from user.forms import *

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponse



# from django.contrib.auth import authenticate, login
# from django.contrib.auth import logout

# # user login
# def my_view(request):
#     email = request.POST['email']
#     password = request.POST['password']
#     user = authenticate(request, email=email, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         context={}
#         #redirect(reverse('home'))
#         return render(request, 'user/ok.html', context)
#     else:
#         # Return an 'invalid login' error message.
#         pass


# def logout_view(request):
#     logout(request)
#     # Redirect to a success page

@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html', {'section': 'dashboard'})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        user = authenticate(request,
                            email = data['email'],
                            password = data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('admin'))
            else:
                return HttpResponse('Account nicht vorhanden.')
        else:
            return HttpResponse('Passwort oder Email falsch.')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def register(request):
    context = {}
    return render(request, 'user/register.html', context)


def dozent(request):
    dozent_form = DozentForm()
    error_message = ""
    if request.POST:
        dozent_form = DozentForm(request.POST)

        if dozent_form.is_valid():
            dozent_form.save()
            return redirect(reverse('ok'))

    context={'form':dozent_form, }
    return render(request, 'user/dozent.html', context)


def module(request):
    module_form = ModuleForm()

    if request.POST:
        module_form = ModuleForm(request.POST)

        if module_form.is_valid():
            module_form.save()
            return redirect(reverse('ok'))

    context = {'form': module_form, }
    return render(request, 'user/form.html', context)


def tutor(request):
    tutor_form = TutorForm()

    if request.POST:
        tutor_form = TutorForm(request.POST)

        if tutor_form.is_valid():
            tutor_form.save()
            return redirect(reverse('ok'))

    context={"form":tutor_form}
    return render(request, 'user/form.html', context)

@login_required
def tutorprofile(request):
    tutor_form = TutorProfileForm()

    if request.POST:
        tutor_form = TutorProfileForm(request.POST)

        if tutor_form.is_valid():
            tutor_form.save()
            return redirect(reverse('ok'))

    context={"form":tutor_form}
    return render(request, 'user/form.html', context)


def kursleiter(request):
    kursleiter_form = KursleiterForm()

    if request.POST:
        kursleiter_form = KursleiterForm(request.POST)

        if kursleiter_form.is_valid():
            kursleiter_form.save()
            return redirect(reverse('ok'))

    context={"form":kursleiter_form}
    return render(request, 'user/form.html', context)


def kursleiterprofile(request):
    kursleiterprofile_form = KursleiterProfileForm()

    if request.POST:
        kursleiterprofile_form = KursleiterProfileForm(request.POST)

        if kursleiterprofile_form.is_valid():
            kursleiterprofile_form.save()
            return redirect(reverse('ok'))

    context={"form":kursleiterprofile_form}
    return render(request, 'user/form.html', context)


def user(request):
    user_form = UserForm()

    if request.POST:
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('ok'))

    context={"form":user_form}
    return render(request, 'user/form.html', context)


# Ok-Seiten zum erfolreichen gespeichern
def ok(request):
    context={}
    return render(request, 'user/ok.html', context)