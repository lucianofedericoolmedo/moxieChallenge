from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from api.models import MedSpa, Service, Appointment, AppointmentStatus
from api.serializers import AppointmentSerializer
from datetime import datetime, time, timedelta

class AppointmentSerializerTests(TestCase):

    def setUp(self):
        # Create test data for MedSpa and Service models
        self.med_spa = MedSpa.objects.create(name='Test MedSpa')
        self.service1 = Service.objects.create(name='Service 1', description='Description 1', price=100.00, duration=30, med_spa=self.med_spa)
        self.service2 = Service.objects.create(name='Service 2', description='Description 2', price=150.00, duration=60, med_spa=self.med_spa)
        self.datetime = timezone.make_aware(datetime(2023, 10, 7, 10, 0))
    def test_create_appointment(self):
        appointment_data = {
            'start_time': self.datetime,  # 10 AM
            'med_spa': self.med_spa.id,
            'services': [self.service1.id, self.service2.id],
            'status': AppointmentStatus.SCHEDULED
        }
        serializer = AppointmentSerializer(data=appointment_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        appointment = serializer.save()

        self.assertEqual(appointment.status, AppointmentStatus.SCHEDULED)
        self.assertEqual(appointment.total_duration, 90)  # 30 + 60
        self.assertEqual(appointment.total_price, 250.00)  # 100 + 150

    def test_create_appointment_exceeds_office_hours(self):
        appointment_data = {
            'start_time': timezone.make_aware(datetime(2023, 10, 7, 17, 30)),  # 5:30 PM
            'med_spa': self.med_spa.id,
            'services': [self.service1.id, self.service2.id],  # 30 + 60 = 90 minutes
            'status': AppointmentStatus.SCHEDULED
        }
        serializer = AppointmentSerializer(data=appointment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_create_appointment_with_invalid_start_time(self):
        appointment_data = {
            'start_time': timezone.make_aware(datetime(2023, 10, 7, 8, 0)),  # 8 AM (invalid)
            'med_spa': self.med_spa.id,
            'services': [self.service1.id],
            'status': AppointmentStatus.SCHEDULED
        }
        serializer = AppointmentSerializer(data=appointment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('start_time', serializer.errors)

    def test_create_appointment_no_services(self):
        appointment_data = {
            'start_time': self.datetime,  # 10 AM
            'med_spa': self.med_spa.id,
            'services': [],
            'status': AppointmentStatus.SCHEDULED
        }
        serializer = AppointmentSerializer(data=appointment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('services', serializer.errors)

    def test_create_appointment_with_status_change(self):
        appointment_services = [self.service1, self.service2]
        sum(service.duration for service in appointment_services)
        # Create an appointment first
        appointment = Appointment.objects.create(
            start_time=self.datetime,
            med_spa=self.med_spa,
            status=AppointmentStatus.SCHEDULED,
            total_duration=sum(service.duration for service in appointment_services)
        )
        appointment.services.set([self.service1, self.service2])

        # Attempt to change the status
        appointment_data = {
            'status': AppointmentStatus.COMPLETED
        }
        serializer = AppointmentSerializer(appointment, data=appointment_data, partial=True)
        self.assertTrue(serializer.is_valid())

    def test_create_appointment_status_default(self):
        appointment_data = {
            'start_time': self.datetime,
            'med_spa': self.med_spa.id,
            'services': [self.service1.id],
            'status': AppointmentStatus.SCHEDULED
        }
        serializer = AppointmentSerializer(data=appointment_data)
        self.assertTrue(serializer.is_valid())
        appointment = serializer.save()
        self.assertEqual(appointment.status, AppointmentStatus.SCHEDULED)

