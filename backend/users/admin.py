from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'password', )
    list_editable = ('password', )
    list_filter = ('email', 'username', )
    search_fields = ('email', 'username', )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', )
    list_editable = ('user', 'author', )
