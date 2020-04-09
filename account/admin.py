from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserDetails


class UserDetailsInLine(admin.StackedInline):
    model = UserDetails


class UserAdminEnhanced(UserAdmin):
    inlines = [UserDetailsInLine]


admin.site.register(User, UserAdminEnhanced)
