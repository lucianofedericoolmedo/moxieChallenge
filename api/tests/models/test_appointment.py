from django.test import TestCase
from django.utils import timezone
from api.models import Appointment, MedSpa, Service, AppointmentServiceRel

class AppointmentModelTest(TestCase):
    def setUp(self):
        """Set up the test case."""
        # Create a MedSpa instance
        self.medspa = MedSpa.objects.create(
            name='Healing Spa',
            address='123 Wellness Ave',
            phone_number='555-1234',
            email='contact@healingspa.com'
        )

        # Create Service instances
        self.service1 = Service.objects.create(
            name='Botox',
            description='Botox injections for facial wrinkles.',
            price=200.00,
            duration=30,
            med_spa=self.medspa
        )
        
        self.service2 = Service.objects.create(
            name='Daxxify',
            description='Daxxify injections for facial wrinkles.',
            price=300.00,
            duration=45,
            med_spa=self.medspa
        )

    def test_create_appointment(self):
        """Test creating an appointment."""
        appointment = Appointment.objects.create(
            start_time=timezone.now(),
            status='scheduled',
            total_duration=75,  # 30 + 45
            total_price=500.00,  # 200 + 300
            med_spa=self.medspa
        )
        
        self.assertIsInstance(appointment, Appointment)
        self.assertEqual(appointment.status, 'scheduled')
        self.assertEqual(appointment.total_duration, 75)
        self.assertEqual(appointment.total_price, 500.00)
        self.assertEqual(appointment.med_spa, self.medspa)

    def test_appointment_services_relationship(self):
        """Test the relationship between Appointment and Service."""
        appointment = Appointment.objects.create(
            start_time=timezone.now(),
            status='scheduled',
            total_duration=75,
            total_price=500.00,
            med_spa=self.medspa
        )

        # Save the appointment first to get its ID
        appointment.save()

        # Create relationships via AppointmentServiceRel
        AppointmentServiceRel.objects.create(appointment=appointment, service=self.service1)
        AppointmentServiceRel.objects.create(appointment=appointment, service=self.service2)

        # Check if services are correctly associated
        self.assertEqual(appointment.services.count(), 2)
        self.assertIn(self.service1, appointment.services.all())
        self.assertIn(self.service2, appointment.services.all())

    def test_update_appointment_status(self):
        """Test updating an appointment's status."""
        appointment = Appointment.objects.create(
            start_time=timezone.now(),
            status='scheduled',
            total_duration=75,
            total_price=500.00,
            med_spa=self.medspa
        )

        # Update status
        appointment.status = 'completed'
        appointment.save()

        self.assertEqual(appointment.status, 'completed')

    def test_appointment_str_method(self):
        """Test the string representation of an appointment."""
        appointment = Appointment.objects.create(
            start_time=timezone.now(),
            status='scheduled',
            total_duration=75,
            total_price=500.00,
            med_spa=self.medspa
        )

        self.assertEqual(str(appointment), f"Appointment at {self.medspa.name} on {appointment.start_time}")
