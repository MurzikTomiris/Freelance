from django.contrib import admin
from .models import Service, Executor, Customer, Order, UserProfile


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'executor', 'description', 'service_type')
# Register your models here.

class ExecutorAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Executor, ExecutorAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Service, ServiceAdmin)
