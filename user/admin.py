from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'weight', 'experience_level')
    search_fields = ('email', 'experience_level')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)