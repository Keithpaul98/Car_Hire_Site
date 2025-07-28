from django.contrib import admin
from .models import Car, Booking, Review

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'daily_rate', 'is_available')
    list_filter = ('is_available', 'make', 'transmission', 'fuel_type')
    search_fields = ('make', 'model')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'status', 'total_cost')
    list_filter = ('status', 'start_date')
    search_fields = ('user__username', 'car__make', 'car__model')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'car__make', 'car__model')
