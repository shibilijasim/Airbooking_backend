from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # user list page
    list_display = ('username', 'email', 'approval_status', 'is_staff')
    list_filter = ('approval_status', 'is_staff', 'is_superuser')
    
    # specific user
    fieldsets = UserAdmin.fieldsets + (
        ('Approval Info', {'fields': ('approval_status',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)