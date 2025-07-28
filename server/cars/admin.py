from django.contrib import admin
from .models import Car, CarCategory, CarFeature, CarImage, Booking, Review

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'category', 'daily_rate', 'is_available')
    list_filter = ('is_available', 'category', 'make', 'transmission', 'fuel_type')
    search_fields = ('make', 'model', 'license_plate')
    inlines = [CarImageInline]
    filter_horizontal = ('features',)

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
