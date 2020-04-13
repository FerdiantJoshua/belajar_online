from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserDetail


class UserDetailInLine(admin.StackedInline):
    model = UserDetail


class UserAdminEnhanced(UserAdmin):
    inlines = [UserDetailInLine]


admin.site.register(User, UserAdminEnhanced)
