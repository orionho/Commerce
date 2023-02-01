from django.contrib import admin

from .models import Item
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title","description","startingbid")

admin.site.register(Item)