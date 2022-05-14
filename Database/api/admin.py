from django.contrib import admin
from api.models import UserModel

class UserModelAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_admin")
    list_display_links = ("id", "username", "is_admin")
    search_fields = ("id", "username", "is_admin")
    list_editable = ("id", "username", "is_admin")
    list_filter = ("id", "username", "is_admin")

admin.site.register(UserModel, UserModelAdmin)