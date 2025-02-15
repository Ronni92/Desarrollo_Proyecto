from django.shortcuts import render
from rest_framework import viewsets
from .models import Evento
from .serializers import EventoSerializer
from rest_framework.permissions import IsAuthenticated

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

def index(request):
    return render(request, 'index.html')
