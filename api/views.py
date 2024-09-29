from datetime import datetime
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import MedSpa, Service, Appointment
from .serializers import ServiceSerializer, AppointmentSerializer

from django.shortcuts import get_object_or_404

class RetrieveUpdateViewSet(viewsets.ViewSet):
    """
    A base ViewSet that allows only PATCH and GET by ID for a specific model.
    """

    def retrieve(self, request, pk=None):
        """Handle GET request for a specific instance."""
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PATCH request for a specific instance."""
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request):
        """Return a method not allowed response for GET all."""
        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, pk=None):
        """Return a method not allowed response for PUT."""
        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AppointmentRetrieveUpdate(RetrieveUpdateViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class ServiceRetrieveUpdate(RetrieveUpdateViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceListCreate(generics.ListCreateAPIView):
    """List all services or create a new service."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        # Ensure that the MedSpa ID is provided in the request data
        med_spa_id = self.request.data.get('med_spa')
        if not MedSpa.objects.filter(id=med_spa_id).exists():
            raise serializers.ValidationError({"med_spa": "MedSpa ID does not exist."})
        serializer.save()


class AppointmentList(generics.ListCreateAPIView):
    """List all appointments."""
    serializer_class = AppointmentSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',  # Name of the query parameter
                openapi.IN_QUERY,  # Location of the parameter
                description="Filter appointments by status",
                type=openapi.TYPE_STRING,  # Type of the parameter
            ),
            openapi.Parameter(
                'start_date',  # Name of the query parameter
                openapi.IN_QUERY,  # Location of the parameter
                description="Filter appointments by start date",
                type=openapi.TYPE_STRING,  # Type of the parameter
                format=openapi.FORMAT_DATE,  # Specify the expected format
            ),
        ]
    )

    def get_queryset(self):
        status_param = self.request.query_params.get('status', None)
        start_time_param = self.request.query_params.get('start_time', None)
        if status_param:
            return Appointment.objects.filter(status=status_param)
        
        if start_time_param:
            start_date = datetime.strptime(start_time_param, '%Y-%m-%d').date()
            return Appointment.objects.filter(start_time__date=start_date)

        return Appointment.objects.all()