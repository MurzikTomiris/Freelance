from django.contrib import admin
from .models import Service, Executor, Customer, Order, UserProfile, OrderRequest


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "executor", "description", "service_type")


class ExecutorAdmin(admin.ModelAdmin):
    list_display = ("profile", "skills", "avatar")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("profile", "preferences")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "price", "order_type")


class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ("order", "executor", "status")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Executor, ExecutorAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderRequest, OrderRequestAdmin)
