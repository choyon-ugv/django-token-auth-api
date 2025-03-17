from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomAdminClass(ModelAdmin):
    pass
