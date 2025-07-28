from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CarViewSet, CarCategoryViewSet, CarFeatureViewSet,
    CarImageViewSet, BookingViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'categories', CarCategoryViewSet)
router.register(r'features', CarFeatureViewSet)
router.register(r'cars', CarViewSet)
router.register(r'cars/(?P<car_pk>\d+)/images', CarImageViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
