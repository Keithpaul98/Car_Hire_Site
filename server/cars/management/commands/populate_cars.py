from django.core.management.base import BaseCommand
from cars.models import Car, CarCategory, CarFeature
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate the database with sample car data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample car data...')

        # Create categories
        suv_category, _ = CarCategory.objects.get_or_create(
            name='SUV',
            defaults={'description': 'Sport Utility Vehicles'}
        )
        sedan_category, _ = CarCategory.objects.get_or_create(
            name='Sedan',
            defaults={'description': 'Comfortable sedan cars'}
        )
        sports_category, _ = CarCategory.objects.get_or_create(
            name='Sports',
            defaults={'description': 'High-performance sports cars'}
        )

        # Create features
        gps_feature, _ = CarFeature.objects.get_or_create(
            name='GPS Navigation',
            defaults={'icon': 'fas fa-map-marked-alt'}
        )
        bluetooth_feature, _ = CarFeature.objects.get_or_create(
            name='Bluetooth',
            defaults={'icon': 'fab fa-bluetooth'}
        )
        ac_feature, _ = CarFeature.objects.get_or_create(
            name='Air Conditioning',
            defaults={'icon': 'fas fa-snowflake'}
        )
        sunroof_feature, _ = CarFeature.objects.get_or_create(
            name='Sunroof',
            defaults={'icon': 'fas fa-sun'}
        )

        # Sample cars data
        cars_data = [
            {
                'make': 'Toyota',
                'model': 'Camry',
                'year': 2023,
                'category': sedan_category,
                'transmission': 'A',
                'fuel_type': 'P',
                'seats': 5,
                'daily_rate': 45.00,
                'weekend_rate': 55.00,
                'description': 'Reliable and comfortable sedan perfect for business trips and family outings.',
                'features': [gps_feature, bluetooth_feature, ac_feature],
                'specifications': {
                    'engine': '2.5L 4-cylinder',
                    'horsepower': '203 hp',
                    'fuel_economy': '32 mpg combined'
                }
            },
            {
                'make': 'Honda',
                'model': 'CR-V',
                'year': 2023,
                'category': suv_category,
                'transmission': 'A',
                'fuel_type': 'P',
                'seats': 5,
                'daily_rate': 55.00,
                'weekend_rate': 65.00,
                'description': 'Spacious SUV with excellent safety ratings and fuel efficiency.',
                'features': [gps_feature, bluetooth_feature, ac_feature, sunroof_feature],
                'specifications': {
                    'engine': '1.5L Turbo 4-cylinder',
                    'horsepower': '190 hp',
                    'fuel_economy': '30 mpg combined'
                }
            },
            {
                'make': 'BMW',
                'model': '3 Series',
                'year': 2023,
                'category': sedan_category,
                'transmission': 'A',
                'fuel_type': 'P',
                'seats': 5,
                'daily_rate': 75.00,
                'weekend_rate': 90.00,
                'description': 'Luxury sedan with premium features and dynamic performance.',
                'features': [gps_feature, bluetooth_feature, ac_feature, sunroof_feature],
                'specifications': {
                    'engine': '2.0L Twin Turbo 4-cylinder',
                    'horsepower': '255 hp',
                    'fuel_economy': '26 mpg combined'
                }
            },
            {
                'make': 'Ford',
                'model': 'Mustang',
                'year': 2023,
                'category': sports_category,
                'transmission': 'M',
                'fuel_type': 'P',
                'seats': 4,
                'daily_rate': 85.00,
                'weekend_rate': 110.00,
                'description': 'Iconic American muscle car with thrilling performance.',
                'features': [gps_feature, bluetooth_feature, ac_feature],
                'specifications': {
                    'engine': '5.0L V8',
                    'horsepower': '450 hp',
                    'fuel_economy': '19 mpg combined'
                }
            },
            {
                'make': 'Tesla',
                'model': 'Model 3',
                'year': 2023,
                'category': sedan_category,
                'transmission': 'A',
                'fuel_type': 'E',
                'seats': 5,
                'daily_rate': 70.00,
                'weekend_rate': 85.00,
                'description': 'Electric sedan with cutting-edge technology and autopilot features.',
                'features': [gps_feature, bluetooth_feature, ac_feature, sunroof_feature],
                'specifications': {
                    'motor': 'Dual Motor All-Wheel Drive',
                    'horsepower': '358 hp',
                    'range': '358 miles'
                }
            },
            {
                'make': 'Jeep',
                'model': 'Wrangler',
                'year': 2023,
                'category': suv_category,
                'transmission': 'M',
                'fuel_type': 'P',
                'seats': 4,
                'daily_rate': 65.00,
                'weekend_rate': 80.00,
                'description': 'Rugged off-road SUV perfect for adventure seekers.',
                'features': [gps_feature, bluetooth_feature, ac_feature],
                'specifications': {
                    'engine': '3.6L V6',
                    'horsepower': '285 hp',
                    'fuel_economy': '22 mpg combined'
                }
            }
        ]

        # Create cars
        for car_data in cars_data:
            features = car_data.pop('features')
            car, created = Car.objects.get_or_create(
                make=car_data['make'],
                model=car_data['model'],
                year=car_data['year'],
                defaults=car_data
            )
            
            if created:
                car.features.set(features)
                self.stdout.write(
                    self.style.SUCCESS(f'Created car: {car.year} {car.make} {car.model}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Car already exists: {car.year} {car.make} {car.model}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample car data!')
        )
