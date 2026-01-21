from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, PassengerViewSet, cache_stats

router = routers.DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'passengers', PassengerViewSet)

urlpatterns = [
    path('cache-stats/', cache_stats, name='cache-stats'),
] + router.urls