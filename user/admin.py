from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import *

# User-View
class UserAdminConfig(UserAdmin):
    list_display = ('username', 'email', 'role',)
    list_filter = ('role',)

    fieldsets = (
        (None, {'fields':('email', 'role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active',)
        }),
    )



# Teacher-View
class TeacherView(UserAdmin):
    list_display = ('username','email', 'role',)

    fieldsets = (
        (None, {'fields':('username', 'email','role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username', 'password1', 'password2',)
        }),
    )

# Teacher-View

class StudentView(UserAdmin):
    list_display = ('username', 'email', 'role',)
    list_filter = ('username', 'email')

    fieldsets = (
        (None, {'fields':('username', 'email', 'role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username', 'password1', 'password2', )
        }),
    )

class StudentProfileView(admin.ModelAdmin):
    list_display = ('user', 'kurs',)
    list_filter = ('kurs',)


class TeacherProfileView(admin.ModelAdmin):
    list_display = ('user', 'module_name',)

class DozentView(admin.ModelAdmin):
    list_display = ('name', 'nachname',)


admin.site.register(Dozent, DozentView)
admin.site.register(Module)
admin.site.register(StudentProfile, StudentProfileView)
admin.site.register(Student, StudentView)
admin.site.register(Teacher, TeacherView)
admin.site.register(TeacherProfile)
admin.site.register(User, UserAdminConfig)