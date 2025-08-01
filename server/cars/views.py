from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q, Avg
from datetime import datetime
from .models import Car, CarCategory, CarFeature, CarImage, Booking, Review
from .serializers import (
    CarSerializer, CarCategorySerializer, CarFeatureSerializer,
    CarImageSerializer, BookingSerializer, ReviewSerializer
)

class CarCategoryViewSet(viewsets.ModelViewSet):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CarFeatureViewSet(viewsets.ModelViewSet):
    queryset = CarFeature.objects.all()
    serializer_class = CarFeatureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(car_id=self.kwargs.get('car_pk'))

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['make', 'model', 'year', 'transmission', 'fuel_type', 'category__name']
    ordering_fields = ['daily_rate', 'year']

    @action(detail=True, methods=['GET'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific car"""
        car = self.get_object()
        avg_rating = Review.objects.filter(car=car).aggregate(Avg('rating'))
        total_bookings = Booking.objects.filter(car=car).count()
        return Response({
            'average_rating': avg_rating['rating__avg'],
            'total_bookings': total_bookings
        })

    @action(detail=False, methods=['GET'])
    def available(self, request):
        """Get available cars for a specific date range"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {"error": "Please provide start_date and end_date parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convert string dates to datetime objects
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get cars that are not booked in the given date range
        unavailable_cars = Booking.objects.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date),
            status__in=['P', 'C', 'A']  # Pending, Confirmed, or Active bookings
        ).values_list('car_id', flat=True)

        available_cars = Car.objects.exclude(id__in=unavailable_cars)
        serializer = self.get_serializer(available_cars, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own bookings"""
        return Booking.objects.filter(user=self.request.user)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        if booking.status in ['P', 'C']:  # Can only cancel Pending or Confirmed bookings
            booking.status = 'CA'
            booking.save()
            serializer = self.get_serializer(booking)
            return Response(serializer.data)
        return Response(
            {"error": "Cannot cancel this booking"},
            status=status.HTTP_400_BAD_REQUEST
        )

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
