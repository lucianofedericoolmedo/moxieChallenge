from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from api.models import MedSpa, Service, Appointment
from api.serializers import ServiceSerializer, AppointmentSerializer
from datetime import datetime

class ServiceViewTests(APITestCase):

    def setUp(self):
        # Create a MedSpa instance
        self.med_spa = MedSpa.objects.create(
            name='Test MedSpa',
            address='123 Test St',
            phone_number='123-456-7890',
            email='test@medspa.com'
        )
        self.service = Service.objects.create(
            name='Service A',
            description='Description A',
            price=100.00,
            duration=30,
            med_spa=self.med_spa
        )

    def test_service_retrieve(self):
        url = reverse('service-retrieve-update', args=[self.service.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.service.name)

    def test_service_update(self):
        url = reverse('service-retrieve-update', args=[self.service.id])
        data = {'name': 'Updated Service A', 'price': 150.00}
        
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Updated Service A')
        self.assertEqual(self.service.price, 150.00)

    def test_service_update_not_found(self):
        url = reverse('service-retrieve-update', args=[999])  # Non-existing ID
        data = {'name': 'Non-existing Service'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_service_create(self):
        url = reverse('service-list-create')
        data = {
            'name': 'Service B',
            'description': 'Description B',
            'price': 200.00,
            'duration': 45,
            'med_spa': self.med_spa.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 2)  # Ensure service was created

    def test_service_create_invalid_medspa(self):
        url = reverse('service-list-create')
        data = {
            'name': 'Service C',
            'description': 'Description C',
            'price': 250.00,
            'duration': 60,
            'med_spa': 999  # Non-existing MedSpa ID
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('med_spa', response.data)

class AppointmentViewTests(APITestCase):

    def setUp(self):
        self.med_spa = MedSpa.objects.create(
            name='Test MedSpa',
            address='123 Test St',
            phone_number='123-456-7890',
            email='test@medspa.com'
        )
        self.service = Service.objects.create(
            name='Service A',
            description='Description A',
            price=100.00,
            duration=30,
            med_spa=self.med_spa
        )
        self.appointment = Appointment.objects.create(
            start_time=timezone.make_aware(datetime.now()),
            status='SCHEDULED',
            total_duration=self.service.duration,
            total_price=self.service.price,
            med_spa=self.med_spa
        )
        self.appointment.services.add(self.service)

    def test_appointment_retrieve(self):
        url = reverse('appointment-retrieve-update', args=[self.appointment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], self.appointment.status)

    def test_appointment_update(self):
        url = reverse('appointment-retrieve-update', args=[self.appointment.id])
        data = {'status': 'COMPLETED'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'COMPLETED')

    def test_appointment_update_not_found(self):
        url = reverse('appointment-retrieve-update', args=[999])  # Non-existing ID
        data = {'status': 'COMPLETED'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_appointment_list(self):
        url = reverse('appointment-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_appointment_list_with_status_filter(self):
        url = reverse('appointment-list') + '?status=SCHEDULED'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_appointment_list_with_date_filter(self):
        url = reverse('appointment-list') + f'?start_time={self.appointment.start_time.date()}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
