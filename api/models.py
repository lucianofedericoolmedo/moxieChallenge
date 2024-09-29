from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class AppointmentStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', 'Scheduled'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class MedSpa(models.Model):
    """Model representing a medical spa center."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    """Model representing a service offered by a MedSpa."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.PositiveIntegerField()  # Duration in minutes

    med_spa = models.ForeignKey(MedSpa, related_name='services', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    """Model representing an appointment at a MedSpa."""
    start_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices)
    total_duration = models.PositiveIntegerField()  # Duration in minutes
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    med_spa = models.ForeignKey(MedSpa, related_name='appointments', on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='AppointmentServiceRel')

    def __str__(self):
        return f"Appointment at {self.med_spa.name} on {self.start_time}"

    def __str__(self):
        return f"Appointment at {self.med_spa.name} on {self.start_time}"

    def save(self, *args, **kwargs):
        # Calculate total_duration and total_price based on related services
        if self.pk:  # Only calculate if the object already exists
            self.total_duration = sum(service.duration for service in self.services.all())
            self.total_price = sum(service.price for service in self.services.all())
        super().save(*args, **kwargs)


class AppointmentServiceRel(models.Model):
    """Join table for many-to-many relationship between Appointments and Services."""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('appointment', 'service')