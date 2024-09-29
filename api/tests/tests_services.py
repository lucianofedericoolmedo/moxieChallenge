from django.test import TestCase
from api.models import MedSpa, Service
from django.core.exceptions import ValidationError

class ServiceModelTest(TestCase):

    def setUp(self):
        """Create a MedSpa instance to use in tests."""
        self.medspa = MedSpa.objects.create(
            name='Healing Spa',
            address='123 Wellness St',
            phone_number='555-0123',
            email='info@healingspa.com'
        )

    def test_create_service(self):
        """Test creating a service record."""
        service = Service.objects.create(
            name='Botox Treatment',
            description='Facial treatment to reduce wrinkles.',
            price=200.00,
            duration=30,
            med_spa=self.medspa  # Correct reference to the MedSpa instance
        )
        
        # Check that the service was created
        self.assertEqual(service.name, 'Botox Treatment')
        self.assertEqual(service.description, 'Facial treatment to reduce wrinkles.')
        self.assertEqual(service.price, 200.00)
        self.assertEqual(service.duration, 30)
        self.assertEqual(service.med_spa, self.medspa)

    def test_create_service_without_medspa(self):
        """Test that creating a service without a MedSpa raises a ValidationError."""
        with self.assertRaises(ValidationError):
            service = Service(
                name='Daxxify Treatment',
                description='Another facial treatment.',
                price=150.00,
                duration=45,
                med_spa=None  # No MedSpa specified
            )
            service.full_clean()  # This will raise a ValidationError

    def test_create_service_with_negative_price(self):
        """Test that creating a service with a negative price raises a ValidationError."""
        with self.assertRaises(ValidationError):
            service = Service(
                name='Invalid Service',
                description='This should not be created.',
                price=-10.00,  # Invalid negative price
                duration=30,
                med_spa=self.medspa
            )
            service.full_clean()  # This will raise a ValidationError


class ServiceModelUpdateTest(TestCase):

    def setUp(self):
        """Create a MedSpa and a Service instance to use in tests."""
        self.medspa = MedSpa.objects.create(
            name='Healing Spa',
            address='123 Wellness St',
            phone_number='555-0123',
            email='info@healingspa.com'
        )
        
        self.service = Service.objects.create(
            name='Botox Treatment',
            description='Facial treatment to reduce wrinkles.',
            price=200.00,
            duration=30,
            med_spa=self.medspa
        )

    def test_update_service(self):
        """Test updating a service record."""
        self.service.name = 'Advanced Botox Treatment'
        self.service.description = 'Enhanced treatment to reduce wrinkles and fine lines.'
        self.service.price = 250.00
        self.service.duration = 45
        self.service.save()  # Save the updated service

        # Refresh the service from the database
        updated_service = Service.objects.get(id=self.service.id)

        # Check that the service was updated correctly
        self.assertEqual(updated_service.name, 'Advanced Botox Treatment')
        self.assertEqual(updated_service.description, 'Enhanced treatment to reduce wrinkles and fine lines.')
        self.assertEqual(updated_service.price, 250.00)
        self.assertEqual(updated_service.duration, 45)

    def test_update_service_invalid_price(self):
        """Test that updating a service with a negative price raises a ValidationError."""
        self.service.price = -10.00  # Invalid negative price

        with self.assertRaises(ValidationError):
            self.service.full_clean()  # This will raise a ValidationError
            self.service.save()  # Attempting to save should also raise an error

    def test_update_service_without_medspa(self):
        """Test that updating a service without a MedSpa raises a ValidationError."""
        self.service.med_spa = None  # Remove the MedSpa association

        with self.assertRaises(ValidationError):
            self.service.full_clean()  # This will raise a ValidationError
            self.service.save()  # Attempting to save should also raise an error


class ServiceModelRetrievalTest(TestCase):

    def setUp(self):
        """Create a MedSpa and several Service instances for testing."""
        self.medspa1 = MedSpa.objects.create(
            name='Healing Spa',
            address='123 Wellness St',
            phone_number='555-0123',
            email='info@healingspa.com'
        )
        
        self.medspa2 = MedSpa.objects.create(
            name='Relaxation Center',
            address='456 Calm Ave',
            phone_number='555-0456',
            email='info@relaxationcenter.com'
        )
        
        self.service1 = Service.objects.create(
            name='Botox Treatment',
            description='Facial treatment to reduce wrinkles.',
            price=200.00,
            duration=30,
            med_spa=self.medspa1
        )
        
        self.service2 = Service.objects.create(
            name='Daxxify Treatment',
            description='Long-lasting wrinkle treatment.',
            price=300.00,
            duration=45,
            med_spa=self.medspa1
        )
        
        self.service3 = Service.objects.create(
            name='Facial Treatment',
            description='Revitalizing facial.',
            price=150.00,
            duration=60,
            med_spa=self.medspa2
        )

    def test_retrieve_services_for_medspa(self):
        """Test retrieving all services for a specific MedSpa."""
        services = Service.objects.filter(med_spa=self.medspa1)

        # Convert the queryset to a list of service names
        service_names = [service.name for service in services]

        # Check that the correct services are returned for medspa1
        expected_services = {'Botox Treatment', 'Daxxify Treatment'}
        self.assertSetEqual(set(service_names), expected_services)

    def test_no_services_for_medspa(self):
        """Test that retrieving services for a MedSpa with no services returns an empty list."""
        services = Service.objects.filter(med_spa=self.medspa2)

        # There should be only one service associated with medspa2
        self.assertEqual(services.count(), 1)

        # Now we check with a non-existent MedSpa
        non_existent_medspa = MedSpa.objects.create(
            name='Non-Existent Spa',
            address='999 Nowhere Rd',
            phone_number='555-9999',
            email='info@nonexistentspa.com'
        )
        services_for_non_existent = Service.objects.filter(med_spa=non_existent_medspa)
        self.assertEqual(services_for_non_existent.count(), 0)

