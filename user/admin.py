from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import *

# User-View
class UserAdminConfig(UserAdmin):
    list_display = ('email', 'vorname', 'nachname', 'role',  'date_published', 'date_modified', )
    list_filter = ('role',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields':('email', 'vorname', 'nachname', 'role', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'vorname', 'nachname', 'role', 'password1', 'password2', 'is_active',)
        }),
    )



# Teacher-View
class KursleiterView(UserAdmin):
    list_display = ('email', 'vorname', 'nachname', 'role', )
    ordering = ('email', )

    fieldsets = (
        (None, {'fields':('vorname', 'nachname', 'email','role', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'vorname', 'nachname', 'password1', 'password2', )
        }),
    )


class TutorView(UserAdmin):
    list_display = ('email', 'vorname', 'nachname', 'role', )
    list_filter = ('email', 'vorname', 'nachname', )
    ordering = ('email', )

    fieldsets = (
        (None, {'fields':('email', 'vorname', 'nachname', 'role', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email','vorname', 'nachname', 'password1', 'password2', )
        }),
    )

class TutorProfileView(admin.ModelAdmin):
    list_display = ('user',)


class KursleiterProfileView(admin.ModelAdmin):
    list_display = ('user', 'module_name',)
    list_filter = ('module', )



admin.site.register(Dozent)
admin.site.register(Kurs)
admin.site.register(TutorProfile, TutorProfileView)
admin.site.register(Tutor, TutorView)
admin.site.register(Kursleiter, KursleiterView)
admin.site.register(KursleiterProfile)
admin.site.register(User, UserAdminConfig)