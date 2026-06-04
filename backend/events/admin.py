from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'date', 'location', 'price', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'artist', 'location')
