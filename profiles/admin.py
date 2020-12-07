from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from profiles.models import MyBooking

User = get_user_model()


# @admin.register(User): the another way to register to admin site
class ProfilesUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'address',
            'year_birth',
            'phone_no',
            'bank_no'
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )


class MyBookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'get_guest', 'check_in', 'check_out', 'price', 'amount')

    def get_guest(self, obj):
        return obj.guest
    get_guest.short_description = 'guest'


admin.site.register(User, ProfilesUserAdmin)
admin.site.register(MyBooking, MyBookingAdmin)




