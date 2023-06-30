from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('steamid', 'nickname', 'user_balance', 'is_staff', 'is_active',)
    list_filter = ('steamid', 'nickname', 'user_balance', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('steamid', 'password', 'nickname', 'user_balance')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('steamid', 'password1', 'nickname', 'user_balance', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('steamid',)
    ordering = ('steamid',)


admin.site.register(CustomUser, CustomUserAdmin)
