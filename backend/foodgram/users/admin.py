from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'pk', 'email', 'password', 'first_name', 'last_name',
    )
    list_editable = ('password', )
    list_filter = ('email','username', )
    search_fields = ('email', 'username', )
    empty_value_display = '-None-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author', )
    empty_value_display = '-None-'
