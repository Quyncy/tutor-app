from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import *

# User-View
class UserAdminConfig(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role',)
    list_filter = ('role',)

    fieldsets = (
        (None, {'fields':('email', 'username', 'first_name', 'last_name','role',)}),
        ('Permissions', {
            'fields':
            ('is_staff', 'is_active','is_superuser',
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active', 'is_staff','is_superuser',)
        }),
    )



# Teacher-View
class TeacherView(UserAdmin):
    list_display = ('username','email', 'first_name', 'last_name', 'role',)

    fieldsets = (
        (None, {'fields':('email', 'username', 'first_name', 'last_name','role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active', 'is_staff','is_superuser',)
        }),
    )

# Teacher-View
class StudentView(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role',)

    fieldsets = (
        (None, {'fields':('email', 'username', 'first_name', 'last_name','role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active', 'is_staff','is_superuser',)
        }),
    )

class StudentProfileView(admin.ModelAdmin):
    list_display = ('user', 'kurs',)
    list_filter = ('kurs',)


class TeacherProfileView(admin.ModelAdmin):
    list_display = ('user')

admin.site.register(Dozent)
admin.site.register(Module)
admin.site.register(StudentProfile, StudentProfileView)
admin.site.register(Student, StudentView)
admin.site.register(Teacher, TeacherView)
admin.site.register(TeacherProfile)
admin.site.register(User, UserAdminConfig)