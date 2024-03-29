from django.contrib import admin
from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'executor', 'description', 'service_type')
# Register your models here.


admin.site.register(Service, ServiceAdmin)
