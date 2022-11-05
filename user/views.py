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


def student(request):
    student_form = StudentForm()

    if request.POST:
        student_form = StudentForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            return redirect(reverse('ok'))

    context={"form":student_form}
    return render(request, 'user/form.html', context)

@login_required
def studentprofile(request):
    student_form = StudentProfileForm()

    if request.POST:
        student_form = StudentProfileForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            return redirect(reverse('ok'))

    context={"form":student_form}
    return render(request, 'user/form.html', context)


def teacher(request):
    teacher_form = TeacherForm()

    if request.POST:
        teacher_form = TeacherForm(request.POST)

        if teacher_form.is_valid():
            teacher_form.save()
            return redirect(reverse('ok'))

    context={"form":teacher_form}
    return render(request, 'user/form.html', context)


def teacherprofile(request):
    teacherprofile_form = TeacherProfileForm()

    if request.POST:
        teacherprofile_form = TeacherProfileForm(request.POST)

        if teacherprofile_form.is_valid():
            teacherprofile_form.save()
            return redirect(reverse('ok'))

    context={"form":teacherprofile_form}
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