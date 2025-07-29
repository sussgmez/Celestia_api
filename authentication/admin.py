from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields':('',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields':('email',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)