from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Inventory, MerchItem, Purchase, Transaction, User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("coins",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("coins",)}),)


admin.site.register(User, CustomUserAdmin)


admin.site.register(MerchItem)
admin.site.register(Inventory)
admin.site.register(Transaction)
admin.site.register(Purchase)
