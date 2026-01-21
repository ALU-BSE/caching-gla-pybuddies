from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from django.conf import settings

from users.models import User, Passenger
from users.serializers import UserSerializer, PassengerSerializer


def get_cache_key(prefix, identifier=None):
    """Generate consistent cache keys"""
    if identifier:
        return f"{prefix}_{identifier}"
    return prefix


@api_view(['GET'])
def cache_stats(request):
    """Get cache statistics"""
    try:
        # Get Redis client
        redis_client = cache._cache.get_client()
        keys = redis_client.keys('*')
        
        return Response({
            'cache_keys': [key.decode() for key in keys],
            'total_keys': len(keys),
            'cache_backend': 'Redis',
            'default_timeout': settings.CACHE_TTL
        })
    except Exception as e:
        return Response({
            'error': str(e),
            'cache_keys': [],
            'total_keys': 0
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key('user_list')
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        return response
    
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        cache_key = get_cache_key('user', user_id)
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        return response
    
    def perform_create(self, serializer):
        cache.delete('user_list')
        super().perform_create(serializer)
    
    def perform_update(self, serializer):
        user_id = serializer.instance.id
        cache.delete('user_list')
        cache.delete(f'user_{user_id}')
        super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        cache.delete('user_list')
        cache.delete(f'user_{instance.id}')
        super().perform_destroy(instance)


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    
    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key('passenger_list')
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        return response
    
    def retrieve(self, request, *args, **kwargs):
        passenger_id = kwargs.get('pk')
        cache_key = get_cache_key('passenger', passenger_id)
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        return response
    
    def perform_create(self, serializer):
        cache.delete('passenger_list')
        super().perform_create(serializer)
    
    def perform_update(self, serializer):
        passenger_id = serializer.instance.id
        cache.delete('passenger_list')
        cache.delete(f'passenger_{passenger_id}')
        super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        cache.delete('passenger_list')
        cache.delete(f'passenger_{instance.id}')
        super().perform_destroy(instance)