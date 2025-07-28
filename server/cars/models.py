from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CarCategory(models.Model):
    name = models.CharField(max_length=50)  # e.g., SUV, Sedan, Sports
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Car Categories"

class CarFeature(models.Model):
    name = models.CharField(max_length=50)  # e.g., GPS, Bluetooth, Sunroof
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class", null=True, blank=True)
    
    def __str__(self):
        return self.name

class CarImage(models.Model):
    car = models.ForeignKey('Car', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.car} - {'Primary' if self.is_primary else 'Secondary'}"

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', 'Automatic'),
        ('M', 'Manual'),
    ]
    
    FUEL_CHOICES = [
        ('P', 'Petrol'),
        ('D', 'Diesel'),
        ('E', 'Electric'),
        ('H', 'Hybrid'),
    ]

    category = models.ForeignKey(CarCategory, on_delete=models.PROTECT, null=True, blank=True)
    features = models.ManyToManyField(CarFeature, blank=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ]
    )
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES)
    seats = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(15)
        ]
    )
    daily_rate = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    weekend_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    mileage = models.IntegerField(help_text="Current mileage of the car", null=True, blank=True)
    license_plate = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    specifications = models.JSONField(
        default=dict,
        help_text="Additional specifications like engine size, horsepower, etc."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('A', 'Active'),
        ('CO', 'Completed'),
        ('CA', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.car} by {self.user.username}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"Review for {self.car} by {self.user.username}"
