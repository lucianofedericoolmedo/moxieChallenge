from django.test import TestCase
from api.models import MedSpa, ServiceProduct, ServiceCategory, ServiceType, ServiceProductSupplier, Service
from api.serializers import ServiceSerializer

class ServiceSerializerTests(TestCase):

    def setUp(self):
        # Create test data for related models
        self.med_spa = MedSpa.objects.create(
            name='Test MedSpa',
            address='123 Test St',
            phone_number='123-456-7890',
            email='test@medspa.com'
        )
        self.service_product = ServiceProduct.objects.create(name='Product A')
        self.service_category = ServiceCategory.objects.create(name='Category A')
        self.service_type = ServiceType.objects.create(name='Type A')
        self.service_product_supplier = ServiceProductSupplier.objects.create(name='Supplier A')

    def test_valid_service_serializer(self):
        service_data = {
            'name': 'Botox Treatment',
            'description': 'Anti-aging treatment',
            'price': 300.00,
            'duration': 30,
            'med_spa': self.med_spa.id,
            'service_product': self.service_product.id,
            'service_category': self.service_category.id,
            'service_type': self.service_type.id,
            'service_product_supplier': self.service_product_supplier.id,
        }
        
        serializer = ServiceSerializer(data=service_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        service = serializer.save()

        # Assertions
        self.assertEqual(service.name, 'Botox Treatment')
        self.assertEqual(service.price, 300.00)
        self.assertEqual(service.duration, 30)
        self.assertEqual(service.med_spa, self.med_spa)
        self.assertEqual(service.service_product, self.service_product)
        self.assertEqual(service.service_category, self.service_category)
        self.assertEqual(service.service_type, self.service_type)
        self.assertEqual(service.service_product_supplier, self.service_product_supplier)

    def test_invalid_service_serializer_missing_fields(self):
        service_data = {
            'name': '',
            'description': 'Missing name test',
            'price': -100.00,  # Invalid price
            'duration': 30,
            'med_spa': self.med_spa.id,
            'service_product': self.service_product.id,
            'service_category': self.service_category.id,
            'service_type': self.service_type.id,
            'service_product_supplier': self.service_product_supplier.id,
        }

        serializer = ServiceSerializer(data=service_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('price', serializer.errors)

    def test_invalid_service_serializer_references(self):
        service_data = {
            'name': 'Invalid Service',
            'description': 'This service references non-existing med spa',
            'price': 150.00,
            'duration': 45,
            'med_spa': 999,  # Non-existent ID
            'service_product': self.service_product.id,
            'service_category': self.service_category.id,
            'service_type': self.service_type.id,
            'service_product_supplier': self.service_product_supplier.id,
        }

        serializer = ServiceSerializer(data=service_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('med_spa', serializer.errors)

    def test_service_serializer_update(self):
        service = Service.objects.create(
            name='Initial Service',
            description='Initial description',
            price=200.00,
            duration=30,
            med_spa=self.med_spa,
            service_product=self.service_product,
            service_category=self.service_category,
            service_type=self.service_type,
            service_product_supplier=self.service_product_supplier,
        )

        updated_data = {
            'name': 'Updated Service',
            'description': 'Updated description',
            'price': 250.00,
            'duration': 45,
            'med_spa': self.med_spa.id,
            'service_product': self.service_product.id,
            'service_category': self.service_category.id,
            'service_type': self.service_type.id,
            'service_product_supplier': self.service_product_supplier.id,
        }

        serializer = ServiceSerializer(service, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_service = serializer.save()

        # Assertions
        self.assertEqual(updated_service.name, 'Updated Service')
        self.assertEqual(updated_service.price, 250.00)
        self.assertEqual(updated_service.duration, 45)

