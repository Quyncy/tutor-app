from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from user.forms import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# @login_required
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

# @login_required
def module(request):
    module_form = ModuleForm()

    if request.POST:
        module_form = ModuleForm(request.POST)

        if module_form.is_valid():
            module_form.save()
            return redirect(reverse('ok'))

    context = {'form': module_form, }
    return render(request, 'user/module.html', context)


def student(request):
    student_form = StudentForm()

    if request.POST:
        student_form = StudentForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            return redirect(reverse('ok'))

    context={"form":student_form}
    return render(request, 'user/form.html', context)


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
    student_form = TeacherForm()

    if request.POST:
        student_form = TeacherForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            return redirect(reverse('ok'))

    context={"form":student_form}
    return render(request, 'user/form.html', context)


def teacherprofile(request):
    student_form = TeacherProfileForm()

    if request.POST:
        student_form = TeacherProfileForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            return redirect(reverse('ok'))

    context={"form":student_form}
    return render(request, 'user/form.html', context)


def user(request):
    student_form = UserForm()

    if request.POST:
        student_form = UserForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            return redirect(reverse('ok'))

    context={"form":student_form}
    return render(request, 'user/form.html', context)





def ok(request):
    context={}
    return render(request, 'user/ok.html', context)