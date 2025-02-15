from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, index

router = DefaultRouter()
router.register(r'eventos', EventoViewSet)

 urlpatterns = [
  path('', index, name='index'),
     path('api/', include(router.urls)),
]