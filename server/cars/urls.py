from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CarViewSet, BookingViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
