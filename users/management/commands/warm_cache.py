from django.core.management.base import BaseCommand
from django.core.cache import cache
from users.models import User, Passenger
from users.serializers import UserSerializer


class Command(BaseCommand):
    help = 'Warm up the cache with frequently accessed data'

    def handle(self, *args, **options):
        # Pre-cache user list
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        cache.set('user_list', serializer.data, timeout=3600)
        
        # Pre-cache individual users
        for user in users:
            user_data = UserSerializer(user).data
            cache.set(f'user_{user.id}', user_data, timeout=3600)
        
        # Pre-cache passengers
        passengers = Passenger.objects.all()
        cache.set('passenger_list', list(passengers.values()), timeout=3600)
        
        for passenger in passengers:
            cache.set(f'passenger_{passenger.id}', {
                'id': passenger.id,
                'user_id': passenger.user_id,
                'passenger_id': passenger.passenger_id,
                'home_address': passenger.home_address
            }, timeout=3600)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cached {len(users)} users and {len(passengers)} passengers')
        )