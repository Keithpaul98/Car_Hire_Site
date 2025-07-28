from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Car, Booking, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    car_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'user', 'car', 'car_id', 'start_date', 'end_date', 
                 'total_cost', 'status', 'created_at', 'updated_at')
        read_only_fields = ('total_cost', 'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Calculate total cost based on number of days and car's daily rate
        car = Car.objects.get(id=validated_data['car_id'])
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        days = (end_date - start_date).days + 1
        total_cost = car.daily_rate * days

        booking = Booking.objects.create(
            user=self.context['request'].user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost,
            status='P'  # Default status is Pending
        )
        return booking

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    car_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'car', 'car_id', 'rating', 'comment', 'created_at')
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        review = Review.objects.create(
            user=self.context['request'].user,
            car_id=validated_data['car_id'],
            rating=validated_data['rating'],
            comment=validated_data['comment']
        )
        return review
