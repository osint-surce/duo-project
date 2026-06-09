from django.contrib import admin
from .models import Event, Category, City, UserProfile, CartItem, Order, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city', 'date', 'price', 'tickets_left')
    list_filter = ('category', 'city', 'date')
    search_fields = ('title', 'description')

    def tickets_left(self, obj):
        return obj.tickets_left
    tickets_left.short_description = 'Осталось билетов'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city')
    search_fields = ('user__username', 'user__email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'event__title')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'added_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'added_at')

